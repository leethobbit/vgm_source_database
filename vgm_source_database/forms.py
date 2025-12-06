"""Forms for VGM Source Database."""

from django import forms


class ImportDataForm(forms.Form):
    """Form for importing YAML fixture files.

    Allows users to upload YAML fixture files for import into the database.
    """

    fixture_file = forms.FileField(
        label="YAML Fixture File",
        help_text="Select a YAML fixture file to import. The file will be validated before import.",
        widget=forms.FileInput(attrs={"accept": ".yaml,.yml"}),
    )
    dry_run = forms.BooleanField(
        label="Dry Run (Validate Only)",
        help_text="Check this to validate the file without importing data.",
        required=False,
        initial=False,
    )
    duplicate_handling = forms.ChoiceField(
        label="Duplicate Handling",
        choices=[
            ("skip", "Skip duplicates (keep existing)"),
            ("overwrite", "Overwrite duplicates (update existing)"),
        ],
        initial="skip",
        help_text="How to handle objects that already exist in the database.",
        required=False,
    )
