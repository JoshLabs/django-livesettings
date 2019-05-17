from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from livesettings import forms
from livesettings.functions import ConfigurationSettings
from livesettings.models import Setting, LongSetting
from livesettings.overrides import get_overrides
import logging

log = logging.getLogger('livesettings.views')
login_url = getattr(settings, 'LS_LOGIN_URL', None)

@csrf_protect
def group_settings(request, group, template='livesettings/group_settings.html'):
    # Determine what set of settings this editor is used for

    use_db, overrides = get_overrides();

    mgr = ConfigurationSettings()
    if group is None:
        settings = mgr
        title = 'Site settings'
    else:
        settings = mgr[group]
        title = settings.name
        log.debug('title: %s', title)

    try:
        setting_version = Setting.objects.latest('version').version
    except Setting.DoesNotExist:
        setting_version = 1
    try:
        long_setting_version = LongSetting.objects.latest('version').version
    except LongSetting.DoesNotExist:
        long_setting_version = 1

    current_version = max(setting_version, long_setting_version)

    if use_db:
        # Create an editor customized for the current user
        # editor = forms.customized_editor(settings)

        if request.method == 'POST':
            # Populate the form with user-submitted data
            data = request.POST.copy()
            version = int(data.pop('version')[0])
            form = forms.SettingsEditor(data, settings=settings)
            if version == current_version:
                if form.is_valid():
                    form.full_clean()
                    with transaction.atomic():
                        for name, value in form.cleaned_data.items():
                            group, key = name.split('__')
                            cfg = mgr.get_config(group, key)
                            if cfg.update(value):

                                # Give user feedback as to which settings were changed
                                messages.add_message(request, messages.INFO, 'Updated %s on %s' % (cfg.key, cfg.group.key))
                        Setting.objects.update(version=current_version + 1)
                        LongSetting.objects.update(version=current_version + 1)

                    return HttpResponseRedirect(request.path)
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'You are on incorrect version of settings. Please refresh the page before updating settings.'
                )
        else:
            # Leave the form populated with current setting values
            # form = editor()
            form = forms.SettingsEditor(settings=settings)
    else:
        form = None

    context = {
        'title': title,
        'group' : group,
        'form': form,
        'use_db' : use_db,
        'version': current_version,
    }
    return render(request, template, context=context)
group_settings = never_cache(permission_required('livesettings.change_setting', login_url)(group_settings))

# Site-wide setting editor is identical, but without a group
# permission_required is implied, since it calls group_settings
def site_settings(request):
    return group_settings(request, group=None, template='livesettings/site_settings.html')

def export_as_python(request):
    """Export site settings as a dictionary of dictionaries"""

    from livesettings.models import Setting, LongSetting
    import pprint

    work = {}
    both = list(Setting.objects.all())
    both.extend(list(LongSetting.objects.all()))

    for s in both:
        sitesettings = work.setdefault(s.site.id, {'DB': False, 'SETTINGS':{}})['SETTINGS']
        sitegroup = sitesettings.setdefault(s.group, {})
        sitegroup[s.key] = s.value

    pp = pprint.PrettyPrinter(indent=4)
    pretty = pp.pformat(work)

    return render(request, 'livesettings/text.txt', context={ 'text' : pretty }, content_type='text/plain')

# Required permission `is_superuser` is equivalent to auth.change_user,
# because who can modify users, can easy became a superuser.
export_as_python = never_cache(permission_required('auth.change_user', login_url)(export_as_python))
