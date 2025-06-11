import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.showCounts', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No active editor');
            return;
        }
        const doc = editor.document;
        const text = doc.getText();
        const lineCount = doc.lineCount;
        const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
        vscode.window.showInformationMessage(`Lines: ${lineCount} Words: ${wordCount}`);
    });
    context.subscriptions.push(disposable);
}

export function deactivate() {}
