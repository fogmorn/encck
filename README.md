# encck
**pre-commit git hook** that checks encoding for each pre-commited file.

## Usage
Rename this script as `pre-commit` put it into `.git/hooks` directory of your project and make it executable.

It will be executed before `git commit` command.

By default only `*.sql` files are checked. You may specify your extension 
of files that you want to check in `EXT` variable.

For `SQL` files there is also added workaround for comment lines and blocks.

## Variables
- `EXT`

   File extension that should be checked.

- `ENC`

   Encoding for checking for.
