# The Enter key — one key, three meanings, and the chat-era confusion

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic.

## The question

Enter used to be predictable. Today, pressing it in a text box either sends a
half-written message or quietly adds a line, depending on the application — and
users cannot know which before they press it. Where did the confusion come
from, and what should a coherent system do?

## The three original meanings

Enter has three legitimate, old meanings, each tied to a kind of control:

1. In a menu, list, or palette, Enter activates the highlighted item. The W3C
   ARIA Authoring Practices keyboard patterns codify this and no product
   disputes it.
2. In a single-line field inside a form, Enter submits the form. This is
   called implicit submission and is written into the HTML standard itself —
   it is why Enter works in every search box and login form ever made. Long-
   standing guidance says to keep it and never suppress it, because users rely
   on it without thinking.
3. In a multi-line text box, Enter inserts a new line. A textarea is a writing
   surface; typing Enter while writing means "new paragraph". Natively, a
   textarea never submits on Enter.

## How chat broke rule 3

Chat applications made Enter send the message and moved the newline to
Shift+Enter, because chat messages are short and sending is the constant
action. The habit spread with the applications — and then leaked into every
comment box, form, and notes field on the web. The result is a permanent split:
long community debates show users evenly and irreconcilably divided over which
behavior is "obvious", which is why some products ended up shipping a user
setting for the key, and others field years-long feature requests to change it.
There is no winning consensus to adopt; there is only a choice to make and
state clearly.

A second convention emerged alongside: Cmd+Enter (Ctrl+Enter on Windows) as
"submit from anywhere", used by code-review and issue-tracking tools for
comment boxes where Enter makes a newline. It is the accelerator that lets both
camps coexist: writers keep Enter as newline, fast submitters get a one-chord
send.

## The reconciliation: the control decides

The coherent rule is not "pick Enter-sends or Enter-newlines for the product";
it is that the kind of control decides the meaning, identically in every
screen:

- Choice surfaces (menus, lists, palettes): Enter activates. Esc closes.
- Single-line form fields: Enter submits — native implicit submission, kept.
- Multi-line text boxes: Enter makes a new line, always. In record-keeping
  applications the text box holds notes and descriptions, not chat; a surprise
  submit of a half-written record is the expensive failure, an extra keystroke
  is the cheap one.
- Cmd/Ctrl+Enter: the one universal "save/submit from anywhere" accelerator.
- Teach it in place: while a text box has focus, the form's primary button
  shows the ⌘↵ hint beside its label. The convention becomes discoverable at
  the exact moment it is useful.
- Shift+Enter: accepted as a harmless newline synonym for chat-trained hands.
- Grids: Enter starts and commits a cell edit, per the standard grid grammar —
  the same control-decides principle on a different control.
- A true chat surface, if one ever exists, is the one place Enter-to-send is
  correct, because that context carries its own learned rule.

## Sources

- HTML Standard — implicit submission (form submission algorithm):
  https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission
- W3C ARIA Authoring Practices Guide — keyboard patterns (menu, listbox, grid):
  https://www.w3.org/WAI/ARIA/apg/patterns/
- Mat Janson Blanchet — The Enter key should submit the form in focus:
  https://jansensan.net/blog/enter-key-should-submit-form-currently-focus
- TJ VanToll — The Enter key should submit forms, stop suppressing it:
  https://www.tjvantoll.com/2013/01/01/enter-should-submit-forms-stop-messing-with-that/
- Hidde de Vries — Form events when submitting with the keyboard:
  https://hidde.blog/form-events-when-submitting-with-keyboard/
- Discourse Meta — Enter to newline vs Shift+Enter to submit (community split):
  https://meta.discourse.org/t/enter-to-newline-shift-enter-to-submit-message-in-chat/289280
- GitLab — configuration option for Enter behavior in chat input:
  https://gitlab.com/gitlab-org/gitlab/-/issues/580601
- Figma forum — request for Cmd/Ctrl+Enter to submit comments:
  https://forum.figma.com/archive-21/allow-cmd-ctrl-enter-to-submit-comments-instead-35970
- Hacker News — discussion of Enter vs Ctrl+Enter inconsistency across apps:
  https://news.ycombinator.com/item?id=47741481
