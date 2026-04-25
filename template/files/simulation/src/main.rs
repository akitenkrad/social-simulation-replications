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
            // TODO: implement run
            // 実行設定を `<output_dir>/config.json` に書き出すこと．
            // `{{NAME}}-tools show-experiment-settings --results-dir <output_dir>` で読み出し可能にする．
            println!("TODO: implement run");
        }
        Commands::Sweep => {
            // TODO: implement sweep
            // スイープ設定を `<output_dir>/sweep_config.json` に書き出すこと．
            println!("TODO: implement sweep");
        }
    }
}
