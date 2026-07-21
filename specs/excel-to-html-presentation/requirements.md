# Requirements: Excel to HTML Presentation

## Introduction
A standalone Python desktop application that turns an Excel spreadsheet into a self-contained HTML slide presentation. A user picks an `.xlsx` file through a simple GUI, the app reads one slide per row using a fixed column convention (Title, Content, Image), and generates a single `.html` file with all styling, scripting, and images inlined — so it can be opened, shared, or emailed as one file with no external dependencies.

## Requirements

### Requirement 1: Select and load a spreadsheet
**User Story:** As a user, I want to pick an Excel file through the app's GUI, so that I don't have to touch a command line or edit config files.

#### Acceptance Criteria
1. WHEN the user clicks "Choose File" THE SYSTEM SHALL open a native file-picker dialog filtered to `.xlsx` files.
2. WHEN the user selects a valid `.xlsx` file THE SYSTEM SHALL load its first worksheet and display the number of slides found before generation.
3. IF the selected file is not a valid `.xlsx` file (wrong format, corrupted) THEN THE SYSTEM SHALL show a clear error message in the GUI and SHALL NOT crash.
4. IF the worksheet has zero data rows THEN THE SYSTEM SHALL show a message indicating there are no slides to generate, rather than producing an empty presentation silently.

### Requirement 2: Parse rows into slides using a fixed column convention
**User Story:** As a user, I want my spreadsheet parsed using a predictable column layout, so that I know exactly how to format my source file.

#### Acceptance Criteria
1. WHEN the worksheet has columns named `Title`, `Content`, and `Image` (header row, case-insensitive) THE SYSTEM SHALL map each subsequent row to one slide with those three fields.
2. WHEN a row's `Content` cell contains multiple lines (line breaks within the cell) THE SYSTEM SHALL render each line as a separate bullet point on that slide.
3. IF a row is missing a `Title` value THEN THE SYSTEM SHALL use a placeholder title (e.g. "Slide N") rather than failing the whole generation.
4. IF a row's `Image` cell is blank THEN THE SYSTEM SHALL generate that slide without an image, rather than treating it as an error.
5. IF the required header columns (`Title`, `Content`) are missing from the worksheet THEN THE SYSTEM SHALL show an error explaining the expected column layout and SHALL NOT attempt to generate a presentation.

### Requirement 3: Generate a single self-contained HTML presentation
**User Story:** As a user, I want one HTML file I can send to anyone, so that they can view my presentation without needing the original spreadsheet or any other files.

#### Acceptance Criteria
1. WHEN generation runs on valid parsed slides THE SYSTEM SHALL produce exactly one `.html` file containing all CSS and JavaScript inlined (no external file references).
2. WHEN a slide has an `Image` value pointing to a local image file THE SYSTEM SHALL embed that image as a base64 data URI inside the HTML rather than linking to the external file path.
3. IF an `Image` path on a row does not resolve to a readable image file THEN THE SYSTEM SHALL generate that slide without the image and SHALL show a warning listing which slide(s) had unresolved images, rather than failing the entire generation.
4. WHEN the HTML presentation is opened in a browser THE SYSTEM SHALL display one slide at a time, navigable via on-screen next/previous controls and left/right arrow keys, with a visible slide-position indicator (e.g. "3 / 8").

### Requirement 4: Trigger generation and choose output location
**User Story:** As a user, I want to choose where the generated HTML file is saved, so that I can find it afterward.

#### Acceptance Criteria
1. WHEN a valid spreadsheet is loaded THE SYSTEM SHALL enable a "Generate" action in the GUI (disabled beforehand).
2. WHEN the user clicks "Generate" THE SYSTEM SHALL open a save-file dialog defaulting to the source spreadsheet's name with a `.html` extension.
3. WHEN generation completes successfully THE SYSTEM SHALL show a confirmation message in the GUI, including the output file path.
4. IF writing the output file fails (e.g. permissions, disk full) THEN THE SYSTEM SHALL show a clear error message and SHALL NOT leave a partially-written file at the target path.

---
**Status:** Approved
