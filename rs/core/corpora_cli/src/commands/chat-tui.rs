use crate::context::Context;
use corpora_client::models::{CorpusChatSchema, MessageSchema};
use crossterm::{
    event::{self, Event, KeyCode, KeyModifiers},
    execute,
    terminal::{self, disable_raw_mode, enable_raw_mode, ClearType},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, Paragraph, Wrap},
    Terminal,
};
use std::io::{self};
use termimad::MadSkin;

// TODO: Unify All Commands to Return Result
// Modify the run functions for all commands (init, sync, etc.)
// to return Result<(), std::io::Error>.
// This aligns with idiomatic Rust practices
// where errors are propagated explicitly.

pub fn run(ctx: &Context) -> io::Result<()> {
    // Initialize terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    let backend = CrosstermBackend::new(&mut stdout);
    let mut terminal = Terminal::new(backend)?;

    // Clear the screen and enter full terminal mode
    execute!(terminal.backend_mut(), terminal::Clear(ClearType::All))?;
    terminal.hide_cursor()?;

    // Chat history and input
    let mut messages: Vec<Line> = vec![Line::from("How can I help you?")];
    let mut input = String::new();
    let mad_skin = create_markdown_skin();

    // Main event loop
    let result = (|| {
        loop {
            terminal.draw(|f| {
                // Split the screen into two sections
                let chunks = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([
                        Constraint::Min(1),    // Chat history
                        Constraint::Length(3), // Input box
                    ])
                    .split(f.area());

                // Chat history
                let chat_history = Paragraph::new(messages.clone())
                    .block(Block::default().borders(Borders::ALL).title("Chat History"))
                    .wrap(Wrap { trim: true });

                f.render_widget(chat_history, chunks[0]);

                // Input editor
                let input_box = Paragraph::new(input.clone())
                    .block(Block::default().borders(Borders::ALL).title("Your Prompt"))
                    .style(Style::default().add_modifier(Modifier::ITALIC));

                f.render_widget(input_box, chunks[1]);
            })?;

            // Handle events
            if let Event::Key(key) = event::read()? {
                match key.code {
                    KeyCode::Char('d') if key.modifiers.contains(KeyModifiers::CONTROL) => {
                        break; // Exit application on Ctrl+D
                    }
                    KeyCode::Char('c') if key.modifiers.contains(KeyModifiers::CONTROL) => {
                        break; // Exit application on Ctrl+C
                    }
                    KeyCode::Char(c) => {
                        input.push(c); // Add character to input
                    }
                    KeyCode::Backspace => {
                        input.pop(); // Remove last character
                    }
                    KeyCode::Enter => {
                        // Submit input and clear the editor
                        if !input.trim().is_empty() {
                            messages.push(Line::from(Span::styled(
                                format!("You: {}", input.trim()),
                                Style::default().add_modifier(Modifier::BOLD),
                            )));
                            let response = process_request(ctx, input.trim());
                            let ai_response = response.unwrap_or_else(|e| format!("Error: {}", e));

                            // Render AI response as Markdown
                            let markdown_response =
                                mad_skin.term_text(ai_response.trim()).to_string();

                            messages.push(Line::from(Span::raw(markdown_response)));
                            input.clear();
                        }
                    }
                    _ => {}
                }
            }
        }
        Ok(())
    })();

    // Cleanup terminal state
    disable_raw_mode()?;
    execute!(terminal.backend_mut(), terminal::LeaveAlternateScreen)?;
    terminal.show_cursor()?;

    result
}

/// Create a Markdown skin for styling AI responses
fn create_markdown_skin() -> MadSkin {
    let skin = MadSkin::default();
    // skin.bold = Style::default().add_modifier(Modifier::BOLD);
    // skin.italic = Style::default().add_modifier(Modifier::ITALIC);
    // skin.inline_code = Style::default().bg(ratatui::style::Color::DarkGray);
    // skin.code_block = Style::default()
    //     .bg(ratatui::style::Color::Black)
    //     .fg(ratatui::style::Color::Green);
    // skin.bullet = Style::default().fg(ratatui::style::Color::Magenta);
    // skin.quote = Style::default().fg(ratatui::style::Color::Blue);
    skin
}

/// Process the user's request and return the assistant's response
fn process_request(ctx: &Context, user_input: &str) -> Result<String, Box<dyn std::error::Error>> {
    let root_path = &ctx.corpora_config.root_path;
    let voice = std::fs::read_to_string(root_path.join(".corpora/VOICE.md")).unwrap_or_default();
    let purpose =
        std::fs::read_to_string(root_path.join(".corpora/PURPOSE.md")).unwrap_or_default();
    let structure =
        std::fs::read_to_string(root_path.join(".corpora/STRUCTURE.md")).unwrap_or_default();

    println!("Voice: {}", voice);
    println!("Purpose: {}", purpose);
    println!("Structure: {}", structure);

    let corpus_id = ctx
        .corpora_config
        .id
        .clone()
        .ok_or("Failed to get corpus ID")?;

    let response = corpora_client::apis::corpus_api::chat(
        &ctx.api_config,
        CorpusChatSchema {
            messages: vec![MessageSchema {
                role: "user".to_string(),
                text: user_input.to_string(),
            }],
            corpus_id,
            voice: Some(voice),
            purpose: Some(purpose),
            structure: Some(structure),
            directions: None,
        },
    )?;

    Ok(response)
}
