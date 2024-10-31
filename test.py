from leads.models import Lead
lead_instance = Lead.objects.get(id=1)  # Change to your specific lead ID
states_string = lead_instance.get_concatenated_states()
print(states_string)  # Output will be a concatenated string of state names