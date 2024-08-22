section .data
    cmd_prompt db "Enter IP Address/URL: ", 0     ; Prompt string for user input
    cmd_prefix db "ping ", 0                      ; Command prefix to initiate ping
    cmd_suffix db " > ping_result.txt", 0         ; Redirect output to a file
    file_open_mode db "r", 0                      ; File open mode (read mode)
    error_message db "Error: Operation failed.", 10, 0 ; Error message string

section .bss
    ip_input resb 256       ; Reserve 256 bytes for user input buffer
    command_buffer resb 512 ; Reserve 512 bytes for constructing the command
    output_buffer resb 1024 ; Reserve 1024 bytes for storing the ping output

section .text
    extern GetStdHandle, WriteFile, ReadFile, CreateFileA, CloseHandle, system, fopen, fgets, printf

    global _start

_start:
    ; Print the prompt to ask for IP/URL input
    push cmd_prompt
    call print_string

    ; Call function to get user input
    call get_input

    ; Validate the input for correct characters
    call validate_input

    ; Construct the command string "ping <input> > ping_result.txt"
    mov edi, command_buffer    ; Destination for the command
    mov esi, cmd_prefix        ; Source: "ping " prefix
    call string_copy           ; Copy the prefix to the command buffer

    mov esi, ip_input          ; Source: user input (IP/URL)
    call string_copy           ; Append user input to command buffer

    mov esi, cmd_suffix        ; Source: suffix to redirect output to file
    call string_copy           ; Append suffix to command buffer

    ; Execute the constructed command using system()
    push command_buffer        ; Push command buffer onto the stack
    call system                ; Call system to execute the ping command

    ; Check if system call was successful
    test eax, eax              ; Test the return value of system call
    jnz system_call_error      ; If non-zero, jump to error handling

    ; Open the ping_result.txt file to read the ping output
    push file_open_mode        ; Push file mode ("r") onto the stack
    push result_file           ; Push filename onto the stack
    call fopen                 ; Call fopen to open the file
    add esp, 8                 ; Clean up stack (remove file mode and name)
    mov esi, eax               ; Store file pointer in esi

    ; Check if the file was successfully opened
    test esi, esi              ; Test if file pointer is NULL
    jz file_open_error         ; If zero (NULL), jump to error handling

    ; Read the content of the file line by line and print it
read_file:
    push output_buffer         ; Push buffer to store each line
    push esi                   ; Push file pointer
    call fgets                 ; Read a line from the file
    test eax, eax              ; Test if end of file is reached (NULL)
    jz done_reading            ; If end of file, jump to done_reading

    ; Print each line read from the file
    push output_buffer         ; Push buffer containing the line
    call print_string          ; Print the line to stdout
    jmp read_file              ; Loop to read the next line

done_reading:
    ; Close the file after reading
    push esi                   ; Push file pointer
    call fclose                ; Call fclose to close the file
    jmp exit                   ; Exit the program

system_call_error:
    ; Handle error if the system call failed
    mov edx, len error_message ; Length of the error message
    mov ecx, error_message     ; Load error message string
    call print_string          ; Print the error message
    jmp exit                   ; Exit the program

file_open_error:
    ; Handle error if file opening failed
    mov edx, len error_message ; Length of the error message
    mov ecx, error_message     ; Load error message string
    call print_string          ; Print the error message
    jmp exit                   ; Exit the program

validate_input:
    ; Validate IP/URL characters in the user input
    mov esi, ip_input          ; Load user input
    .next_char:
        lodsb                  ; Load next byte from input
        cmp al, 0              ; Check for end of string
        je .done_validation    ; If end, jump to done_validation
        cmp al, '0'            ; Check if character is a digit or letter
        jl input_invalid       ; If less than '0', input is invalid
        cmp al, '9'
        jle .next_char         ; If within '0' to '9', continue
        cmp al, '.'
        je .next_char          ; If '.', continue
        cmp al, '-'
        je .next_char          ; If '-', continue
        cmp al, 'a'
        jl input_invalid       ; If less than 'a', input is invalid
        cmp al, 'z'
        jle .next_char         ; If within 'a' to 'z', continue
        cmp al, 'A'
        jl input_invalid       ; If less than 'A', input is invalid
        cmp al, 'Z'
        jle .next_char         ; If within 'A' to 'Z', continue
        jmp input_invalid      ; If invalid character, jump to error

    .done_validation:          ; Label for end of validation
        ret                    ; Return to caller

    input_invalid:
        ; Handle invalid input error
        mov edx, len error_message ; Length of the error message
        mov ecx, error_message     ; Load error message string
        call print_string          ; Print the error message
        jmp exit                   ; Exit the program

string_copy:
    ; Copy string from [esi] to [edi]
    .next_char_copy:
        lodsb                  ; Load next byte from source
        stosb                  ; Store byte into destination
        test al, al            ; Check if end of string
        jnz .next_char_copy    ; If not end, continue copying
    ret                        ; Return to caller

get_input:
    ; Zero out the input buffer to avoid leftover data
    mov edi, ip_input          ; Load destination address
    mov ecx, 255               ; Set counter (max input length minus one)
    xor eax, eax               ; Set fill value (0)
    rep stosb                  ; Fill buffer with zeros

    ; Read the user input from stdin
    mov edi, ip_input          ; Load destination address
    mov ecx, 255               ; Set counter (max input length minus one)
    .next_char_input:
        call getchar           ; Read a character from stdin
        cmp al, 0x0A           ; Check if newline character
        je .done_input         ; If newline, end input
        stosb                  ; Store the character in the buffer
        loop .next_char_input  ; Loop for the next character
    .done_input:
        stosb                  ; Null-terminate the string
    ret                        ; Return to caller

print_string:
    ; Print a null-terminated string at [esp+4]
    mov eax, 4                 ; Syscall number for sys_write
    mov ebx, 1                 ; File descriptor for stdout
    mov ecx, [esp+4]           ; Load address of the string
    call strlen                ; Get string length
    mov edx, eax               ; Set length for write
    int 0x80                   ; Make syscall
    ret                        ; Return to caller

strlen:
    ; Calculate the length of a null-terminated string in ecx
    xor eax, eax               ; Clear eax (string length counter)
    .next_char_strlen:
        lodsb                  ; Load next byte from string
        test al, al            ; Check if end of string
        jz .done_strlen        ; If end, finish
        inc eax                ; Increment counter
        jmp .next_char_strlen  ; Continue counting
    .done_strlen:
        ret                    ; Return string length in eax

exit:
    ; Exit the program
    mov eax, 1                 ; Syscall number for sys_exit
    xor ebx, ebx               ; Exit code 0
    int 0x80                   ; Make syscall