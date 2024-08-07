use std::net::{TcpStream, ToSocketAddrs};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Duration;

fn scan_port(tx: mpsc::Sender<u16>, ip: Arc<String>, port: u16) {
    let addr = format!("{}:{}", ip, port);
    if TcpStream::connect_timeout(&addr,to_socket_addrs().unrap().next().unrwap(), Duration::from_secs(1)).is_ok(){
        tx.send(port).unrwap();
    }
}

fn main() {
    let target_ip = Arc::new("scanme.nmap.org".to_string());
    let (tx, rx) = mpsc::channel();
    let open_ports = Arc::new(Mutex::new(Vec::new()));

    for port in 1..1025 {
        let tx = tx.clone();
        let ip = Arc::clone(&target_ip);
        let open_ports = Arc::clone(&open_ports);

        thread::spawn(move || {
            scan_port(tx, ip, port);
        });

        match rx.recv_timeout(Duration::from_secs(1)) {
            Ok(port) => {
                let mut open_ports = open_ports.lock().unwrap();
                open_ports.push(port);
            }
            Err(_) => {}
        }
    }

    let open_ports = open_ports.lock().unwrap();
    for port in open_ports.iter() {
        println!("Port {} is open", port);
    }
}