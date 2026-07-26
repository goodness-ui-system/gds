# Record Forms — the screen behind the row

> Research briefing. Sources are cited inline where claims are made and listed at
> the end. The two layouts at the close are encoded in `components.md` §3.7 and
> rendered in `specimen.html`.

## The question

A user clicks a row in a table and a record opens: a group of fields, each with a
label. The common industry habit renders every field or field-group as a card —
exactly the clutter the sections principle exists to kill. What should this
screen be instead, and is one layout enough?

## The finding that organizes everything: read and write are different tasks

The apparent contradictions in the form literature dissolve once entry and
review are separated. The foundational eye-tracking work found labels placed
above fields are captured together with the field in a single ~50ms eye
movement — the fastest arrangement for filling — while left-aligned side labels
cost ~500ms of eye travel per field (Penzo, UXmatters 2006). Yet the same
left-aligned column that slows entry is what makes a record scannable: readers
run down the label column to locate a field and compare values, which is hard
to do when labels sit above fields (Jarrett, Effortmark). Enterprise systems
encode the same split — a major CRM's comfortable density puts labels above
fields while its compact density puts them beside fields on record detail, and
the read-only description-list components of the major design systems default
to horizontal label:value rows. Conclusion: an entry form and a record view are
two different components.

## The evidence, by decision

Labels. Top-aligned, regular weight, sentence case for entry forms — bold
labels measurably slow reading, and floating or placeholder labels are harmful
(users lose the label once typing starts; fields look pre-filled; NN/g).
Left-aligned muted label columns for read-first records, with a fixed label
width so values form their own clean scan line.

Columns. Single column for entry: multi-column forms complete ~15 seconds
slower in controlled research (CXL/Speero) and cause sequence misinterpretation
and skipped fields (Baymard). The one sanctioned exception: short fields that
form a single conceptual entity — city and postal code, date parts — may share
a line. Read-only property rows are exempt from the single-column evidence,
which is about entry momentum, not display.

Grouping. Related fields chunk into sections separated by white space and a
small header — proximity does the grouping, not boxes (NN/g). Spacing between
groups must be visibly larger than spacing within them. This is the sections
principle applied to forms: full-bleed field groups sharing one hairline, never
a card per field or per group. The leading issue-tracker's redesign states the
direction plainly: reduce visual noise, increase density.

Editing model. Three patterns exist: an always-editable form, a view mode with
an explicit edit switch, and per-field click-to-edit. The written guidance
(PatternFly) fits the property sheet exactly: inline edit suits data updated
frequently where editing is not the view's primary function; escalate to a
form when editing is the primary task or fields are interdependent. The commit
rule that reconciles autosave and explicit save (GitHub Primer): constrained
pickers — status, owner, dates, enums — commit instantly on selection;
free-text edits get an in-place input with adjacent confirm and cancel;
multi-field transactions escalate to the entry form. Never mix commit models
within one surface.

Actions. Buttons at the bottom, secondary left of primary, primary named with
a verb ("Save changes", never "OK"); no reset button, ever — the risk of
accidental erasure outweighs the rare need (NN/g). For long forms the footer
is sticky (the enterprise floorplans keep finalizing actions in a footer bar
that never scrolls away). Destructive record actions live in the header
overflow menu under the consequential-action rule, never beside Save.

Validation. Never while the user is still typing a first entry; on leaving the
field is acceptable, and errors sit directly under the field they belong to
(Baymard; NN/g). On submit, long forms add a summary at the top that repeats —
never replaces — the field-level messages, with identical wording (GOV.UK).
Input is always preserved. In the property sheet, only one field is ever in
flight, so validation is per-commit and in place.

## The two canonical layouts

Layout 1, the entry/edit form — for creating a record or an explicit edit mode
where cross-field validation matters. Top-aligned regular-weight labels;
strict single column (~40–48ch inputs) with the conceptual-pair exception;
hairline-separated sections with small headers; sticky footer with Cancel then
Save changes; explicit save (declarative input); on-blur validation plus a
submit-time summary.

Layout 2, the property sheet — the default screen behind a clicked row, read
first. Identity header (title plus a few pinned key facts), then hairline
label:value rows: fixed muted label column left, value carrying the visual
weight right, numbers and dates in mono. Whole row is the edit target; hover
reveals the affordance; pickers commit instantly, text opens in place with
confirm/cancel; anything transactional escalates to Layout 1 in a dialog or
panel. No save footer — nothing is ever pending. Record-level actions sit in
the header menu, destructive ones separated per the consequential-action rule.

The two are a system, not rivals: the sheet is where records live; the form is
where records are born and where complex edits go.

## Sources

- Penzo, Label Placement in Forms (eye-tracking, 2006):
  https://www.uxmatters.com/mt/archives/2006/07/label-placement-in-forms.php
- Jarrett, Label placement in forms — the scanning counterpoint:
  https://www.effortmark.co.uk/label-placement-forms-whats-best/
- NN/g, Website Forms Usability top 10: https://www.nngroup.com/articles/web-form-design/
- NN/g, Placeholders in form fields are harmful:
  https://www.nngroup.com/articles/form-design-placeholders/
- NN/g, Group form elements with white space:
  https://www.nngroup.com/articles/form-design-white-space/
- NN/g, Reporting errors in forms: https://www.nngroup.com/articles/errors-forms-design-guidelines/
- Baymard, Avoid multicolumn forms: https://baymard.com/blog/avoid-multi-column-forms
- Baymard, Inline form validation testing: https://baymard.com/blog/inline-form-validation
- CXL/Speero, single- vs multi-column research:
  https://speero.com/post/form-field-usability-should-you-use-single-or-multi-column-forms-original-research
- PatternFly, Inline edit guidelines: https://www.patternfly.org/components/inline-edit/design-guidelines/
- PatternFly, Description list guidelines: https://www.patternfly.org/components/description-list/design-guidelines/
- GitHub Primer, Saving patterns (declarative vs imperative commit):
  https://primer.style/product/ui-patterns/saving/
- GOV.UK Design System, Error message + summary:
  https://design-system.service.gov.uk/components/error-message
- Carbon Design System, Forms pattern: https://v10.carbondesignsystem.com/patterns/forms-pattern/
- Linear, How the UI was redesigned (noise reduction, density):
  https://linear.app/now/how-we-redesigned-the-linear-ui
- Salesforce lightning-record-form (density label placement, view/edit modes):
  https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-record-form.html
- Scott & Neil, Designing Web Interfaces, In-Page Editing:
  https://www.oreilly.com/library/view/designing-web-interfaces/9780596155353/ch01.html
