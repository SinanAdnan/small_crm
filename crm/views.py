from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

def settings_view(request):
    if request.method == 'POST':
        # Process the settings form submission
        setting1 = request.POST.get('setting1')
        setting2 = request.POST.get('setting2')
        # Save the settings (this example assumes you're saving to Django settings)
        # In a real implementation, you might save to a database or configuration file
        settings.SETTING1 = setting1
        settings.SETTING2 = setting2
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    else:
        # Load the current settings
        current_settings = {
            'setting1': getattr(settings, 'SETTING1', ''),
            'setting2': getattr(settings, 'SETTING2', ''),
        }
    return render(request, 'settings.html', {'settings': current_settings})