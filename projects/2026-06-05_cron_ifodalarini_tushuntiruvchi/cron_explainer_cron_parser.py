import collections

# Constants for cron field definitions:
# (field_name, min_value, max_value, optional_name_map)
FIELD_DEFINITIONS = [
    ("minute", 0, 59, None),
    ("hour", 0, 23, None),
    ("day of month", 1, 31, None),
    ("month", 1, 12, collections.OrderedDict([
        (1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"),
        (7, "July"), (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December")
    ])),
    ("day of week", 0, 7, collections.OrderedDict([ # 0 and 7 are both Sunday
        (0, "Sunday"), (1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"),
        (5, "Friday"), (6, "Saturday"), (7, "Sunday") 
    ]))
]

def _get_numeric_value_from_str(value_str, field_name, min_val, max_val, names_map=None):
    """
    Converts a cron field part string (e.g., "1", "JAN", "MON") to its numeric equivalent.
    Performs range validation. Returns (numeric_value, error_message) tuple.
    """
    try:
        val = int(value_str)
        if not (min_val <= val <= max_val):
            return None, f"Value '{value_str}' out of range ({min_val}-{max_val}) for {field_name}"
        return val, None
    except ValueError:
        if names_map:
            # Try to match string names (JAN, FEB, SUN, MON etc.)
            name_to_val = {v.upper(): k for k, v in names_map.items()}
            if value_str.upper() in name_to_val:
                val = name_to_val[value_str.upper()]
                return val, None
        return None, f"Invalid {field_name} value '{value_str}'"

def _get_display_name(value, names_map=None):
    """
    Returns the human-readable name for a given numeric cron value (e.g., 1 -> "January").
    """
    if names_map and isinstance(value, int) and value in names_map:
        return names_map[value]
    return str(value)

def _parse_single_value_field(field_str, field_name, min_val, max_val, names_map=None):
    """
    Parses a single cron value (e.g., "5", "JAN") and returns its description.
    """
    val, error = _get_numeric_value_from_str(field_str, field_name, min_val, max_val, names_map)
    if error:
        return f"Error: {error}"
    return _get_display_name(val, names_map)

def _parse_range_or_list_field(field_str, field_name, min_val, max_val, names_map=None):
    """
    Parses a cron field string containing a range (e.g., "1-5") or a list (e.g., "1,3,5").
    """
    if ',' in field_str:
        values = []
        for v_str in field_str.split(','):
            val, error = _get_numeric_value_from_str(v_str, field_name, min_val, max_val, names_map)
            if error: return f"Error: {error}" # Propagate error
            values.append(_get_display_name(val, names_map))
        return f"on {', '.join(values)}"
    elif '-' in field_str:
        start_str, end_str = field_str.split('-')
        start_val, error = _get_numeric_value_from_str(start_str, field_name, min_val, max_val, names_map)
        if error: return f"Error: {error}"
        end_val, error = _get_numeric_value_from_str(end_str, field_name, min_val, max_val, names_map)
        if error: return f"Error: {error}"
        
        start_display = _get_display_name(start_val, names_map)
        end_display = _get_display_name(end_val, names_map)
        return f"from {start_display} through {end_display}"
    return f"Error: Unexpected format '{field_str}' for {field_name} (expected range or list)"

def _parse_base_cron_value(value_str, field_name, min_val, max_val, names_map=None):
    """
    Helper to parse the base part of a step expression (e.g., '1-5' in '1-5/2').
    It handles single values, ranges, or lists, but not steps or special characters.
    It returns just the value description, without "on ".
    """
    if '-' in value_str or ',' in value_str:
        # For ranges/lists, parse them and adjust the "on " / "from " prefix if needed.
        # This is primarily for constructing the 'starting X' part of step expressions.
        parsed_desc = _parse_range_or_list_field(value_str, field_name, min_val, max_val, names_map)
        if parsed_desc.startswith("on "):
            return parsed_desc[3:] # Remove "on "
        return parsed_desc
    else:
        # For single values, just return the display name.
        val, error = _get_numeric_value_from_str(value_str, field_name, min_val, max_val, names_map)
        if error: return f"Error: {error}"
        return _get_display_name(val, names_map)


def _parse_field(field_str, field_name, min_val, max_val, names_map=None):
    """
    Parses a single cron field string and returns a human-readable description.
    Handles all cron special characters and value types for a given field.
    """
    field_name_key = field_name.replace(' ', '_') # Internal key for special logic

    # 1. Handle special '?'
    if field_str == '?':
        return f"no specific {field_name}"

    # 2. Handle specific day_of_month/day_of_week patterns (L, W, #)
    if field_name_key == "day_of_month":
        if field_str == "L":
            return "on the last day of the month"
        if field_str.endswith("W"):
            day_num_str = field_str[:-1]
            day_num, error = _get_numeric_value_from_str(day_num_str, field_name, min_val, max_val, names_map)
            if error: return f"Error: {error}"
            return f"on the nearest weekday to day {day_num}"
    elif field_name_key == "day_of_week":
        if field_str.endswith("L"):
            day_num_str = field_str[:-1]
            day_num, error = _get_numeric_value_from_str(day_num_str, field_name, min_val, max_val, names_map)
            if error: return f"Error: {error}"
            day_name = _get_display_name(day_num, names_map)
            return f"on the last {day_name} of the month"
        if '#' in field_str:
            try:
                day_num_str, occurrence_str = field_str.split('#')
                day_num, error = _get_numeric_value_from_str(day_num_str, field_name, min_val, max_val, names_map)
                if error: return f"Error: {error}"
                occurrence = int(occurrence_str)
                if not (1 <= occurrence <= 5): # Common range for occurrence
                    return f"Error: Occurrence '{occurrence_str}' out of typical range (1-5) for '#' in {field_name}"

                day_name = _get_display_name(day_num, names_map)
                ordinals = ["first", "second", "third", "fourth", "fifth"]
                occurrence_desc = ordinals[occurrence - 1] if 1 <= occurrence <= len(ordinals) else f"{occurrence}th"
                return f"on the {occurrence_desc} {day_name} of the month"
            except (ValueError, IndexError):
                return f"Error: Invalid format for '#' in {field_name}: '{field_str}'"

    # 3. Handle step '/'
    if '/' in field_str:
        try:
            base_str, step_str = field_str.split('/')
            step = int(step_str)
            if step <= 0: return f"Error: Invalid step value '{step_str}' for {field_name}"

            if base_str == '*':
                return f"every {step} {field_name}"
            else:
                # Parse the base part which can be a range or list or single value
                base_description = _parse_base_cron_value(base_str, field_name, min_val, max_val, names_map)
                if base_description.startswith("Error:"):
                    return base_description # Propagate error
                
                # Adjust wording for combined step and base
                if base_description.startswith("from "):
                    # e.g., "every 2 minutes from 10 through 20"
                    return f"every {step} {field_name} {base_description}"
                elif base_description:
                    # e.g., "every 5 minutes starting 10" (for "10/5") or "every 2 minutes on 1,3,5" (for "1,3,5/2")
                    return f"every {step} {field_name} starting {base_description}"
                else:
                    return f"every {step} {field_name}" # Should not happen unless base_description is empty for some reason
        except (ValueError, IndexError):
            return f"Error: Invalid step format for {field_name}: '{field_str}'"

    # 4. Handle range '-' or list ','
    if '-' in field_str or ',' in field_str:
        return _parse_range_or_list_field(field_str, field_name, min_val, max_val, names_map)

    # 5. Handle '*'
    if field_str == '*':
        return f"every {field_name}"

    # 6. Handle single value (numeric or named)
    description = _parse_single_value_field(field_str, field_name, min_val, max_val, names_map)
    if description.startswith("Error:"):
        return description
    return f"on {description}"

def explain_cron_expression(cron_string):
    """
    Explains a 5-field cron expression in human-readable terms.
    Returns a dictionary with 'summary' and 'details' (list of strings).
    """
    fields = cron_string.split()
    if len(fields) != 5:
        return {
            "summary": "Error: Invalid cron expression format.",
            "details": ["Cron expression must have exactly 5 fields (minute, hour, day of month, month, day of week)."]
        }

    explanations = []
    
    for i, field_def in enumerate(FIELD_DEFINITIONS):
        field_name, min_val, max_val, names_map = field_def
        field_str = fields[i]
        
        description = _parse_field(field_str, field_name, min_val, max_val, names_map)
        explanations.append((field_name, description)) # Store name and description

    # Check for any errors in explanations
    has_errors = False
    for _, desc in explanations:
        if desc.startswith("Error:"):
            has_errors = True
            break
            
    if has_errors:
        error_details = [f"- {name.capitalize()}: {desc}" for name, desc in explanations if desc.startswith("Error:")]
        return {
            "summary": "Error: Failed to parse cron expression.",
            "details": error_details
        }

    # Generate a more concise and readable summary sentence
    minute_summary = explanations[0][1]
    hour_summary = explanations[1][1]
    dom_summary = explanations[2][1]
    month_summary = explanations[3][1]
    dow_summary = explanations[4][1]

    # Rephrase parts for better flow in a single summary sentence
    # Minute
    if minute_summary.startswith("on "): 
        minute_val_str = minute_summary[3:]
        # Try converting to int to add "minutes past the hour" if possible
        try:
            minute_val = int(minute_val_str)
            minute_summary = f"at {minute_val} minutes past the hour"
        except ValueError:
            minute_summary = f"at {minute_val_str} minutes past the hour"
    elif minute_summary == "every minute": minute_summary = "every minute"
    elif minute_summary.startswith("every "): minute_summary = f"at {minute_summary} past the hour"
    elif minute_summary == "no specific minute": minute_summary = "at any minute"

    # Hour
    if hour_summary.startswith("on "):
        hour_val_str = hour_summary[3:]
        try:
            hour_val = int(hour_val_str)
            ampm = "AM" if hour_val < 12 else "PM"
            hour_val_12 = hour_val if hour_val <= 12 else hour_val - 12
            if hour_val_12 == 0: hour_val_12 = 12 # Midnight is 12 AM
            hour_summary = f"at {hour_val_12} {ampm}"
        except ValueError:
            hour_summary = f"at {hour_val_str} o'clock" # Fallback for complex hour strings
    elif hour_summary == "every hour": hour_summary = "every hour"
    elif hour_summary.startswith("every "): hour_summary = f"at {hour_summary}"
    elif hour_summary == "no specific hour": hour_summary = "at any hour"

    # Day of month
    if dom_summary.startswith("on the last day"): pass
    elif dom_summary.startswith("on the nearest weekday"): pass
    elif dom_summary.startswith("on "): dom_summary = f"on the {dom_summary[3:]} day of the month"
    elif dom_summary == "every day of month": dom_summary = "every day of the month"
    elif dom_summary.startswith("every "): dom_summary = f"on {dom_summary}"
    elif dom_summary == "no specific day of month": dom_summary = "on any day of the month"

    # Month
    if month_summary.startswith("on "): month_summary = f"in {month_summary[3:]}"
    elif month_summary == "every month": month_summary = "every month"
    elif month_summary.startswith("every "): month_summary = f"in {month_summary}"
    elif month_summary == "no specific month": month_summary = "in any month"

    # Day of week
    if dow_summary.startswith("on the last "): pass # e.g., "on the last Sunday of the month"
    elif dow_summary.startswith("on the "): pass # e.g., "on the first Monday of the month"
    elif dow_summary.startswith("on "): dow_summary = f"on {dow_summary[3:]}"
    elif dow_summary == "every day of week": dow_summary = "every day of the week"
    elif dow_summary.startswith("every "): dow_summary = f"on {dow_summary}"
    elif dow_summary == "no specific day of week": dow_summary = "on any day of the week"
    
    # Combine the rephrased parts into a single summary sentence
    combined_summary = (
        f"Scheduled to run {minute_summary}, {hour_summary}, "
        f"{dom_summary}, {month_summary}, and {dow_summary}."
    )

    return {
        "summary": combined_summary.capitalize(),
        "details": [f"- {name.capitalize()}: {desc}" for name, desc in explanations]
    }