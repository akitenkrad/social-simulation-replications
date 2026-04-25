use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(name = "{{NAME}}", about = "Simulation entry point")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// 単一シミュレーションを実行する
    Run,
    /// パラメータスイープを実行する
    Sweep,
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Run => {
            println!("TODO: implement run");
        }
        Commands::Sweep => {
            println!("TODO: implement sweep");
        }
    }
}
