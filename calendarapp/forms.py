from calendarapp.models import Event, EventCategory
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm


class EventModalForm(BSModalModelForm):
    """Event form using Bootstrap Modal, for creating and editing events."""

    class Meta:
        model = Event
        fields = ["category", "title", "description", "all_day", "start_date", "start_time", "end_date", "end_time", 
        "planned_exertion"] # Only selects the relevant fields for creating a new event
        # Adding custom widgets for each field, i.e. to add CSS classes
        widgets = {
            "category": forms.Select(
                attrs={"class": "form-control"},
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control form-control-lg", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter event description"}
            ),
            "all_day": forms.CheckboxInput(
                attrs={"style": "margin-left: 5px; margin-right: 5px;"}
            ),
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control", "style": "width: 100%;"},
                format="%Y-%m-%d",
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control", "style": "width: 100%;"},
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control", "style": "width: 100%;"},
                format="%Y-%m-%d",
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control", "style": "width: 100%;"},
            ),
            "planned_exertion": forms.NumberInput(
                attrs={"type": "range", "class": "align-middle", "step": "1", "min": "1", "max": "10", "value": "0",
                       "style": "width: 45%;"},
            ),
        }

    def __init__(self, *args, **kwargs):
        """Adds initial values for start and end dates using the date from the form kwargs."""
        date = kwargs.pop("date", None)
        super(EventModalForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].initial = date
        self.fields["end_date"].initial = date


class EventDetailsModalForm(BSModalModelForm):
    """Event form using Bootstrap Modal, for updating an event after it has occurred."""

    class Meta:
        model = Event
        # Only selects the relevant fields for updating a post event
        fields = ["is_post", "post_rating", "post_exertion", "post_fb_neg", "post_fb_pos", "post_comments"]
        # Adding custom widgets for each field, i.e. to add CSS classes
        widgets = {
            "post_rating": forms.RadioSelect(
                choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
            ),
            "post_exertion": forms.NumberInput(
                attrs={"type": "range", "step": "1", "min": "1", "max": "10", "value": "0",
                       "style": "width: 90%;"},
            ),
            "post_fb_neg": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter attention points"},
            ),
            "post_fb_pos": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter positive points"},
            ),
            "post_comments": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter notes"},
            ),
        }


class EventCategoryForm(forms.ModelForm):
    """EventCategory form using Bootstrap Modal, for creating categories."""
    
    class Meta:
        model = EventCategory
        fields = ["name", "parent_category"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter category name", "style": "max-width: 300px;"},
            ),
            "parent_category": forms.Select(
                attrs={"class": "form-control", "style": "max-width: 300px;"},
            ),
        }
