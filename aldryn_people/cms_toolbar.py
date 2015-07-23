# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext as _, get_language_from_request

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from .models import Group, Person


@toolbar_pool.register
class PeopleToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Person, ]
    supported_apps = ('aldryn_people', )

    def populate(self):
        user = getattr(self.request, 'user', None)
        if user:
            language = get_language_from_request(self.request, check_path=True)
            view_name = self.request.resolver_match.view_name
            kwargs = self.request.resolver_match.kwargs
            if view_name == 'aldryn_people:group-detail':
                group = (Group.objects
                              .translated(language, slug=kwargs['slug'])
                              .first())
                person = None
            elif view_name == 'aldryn_people:person-detail':
                person = Person.objects.filter(slug=kwargs['slug']).first()
                group = person.group
            else:
                group = person = None

            menu = self.toolbar.get_or_create_menu('people-app', "People")
            change_group_perm = user.has_perm('aldryn_people.change_group')
            add_group_perm = user.has_perm('aldryn_people.add_group')
            group_perms = [change_group_perm, add_group_perm]

            change_person_perm = user.has_perm('aldryn_people.change_person')
            add_person_perm = user.has_perm('aldryn_people.add_person')
            person_perms = [change_person_perm, add_person_perm]

            if change_group_perm:
                menu.add_sideframe_item(
                    _('Group list'),
                    url=admin_reverse('aldryn_people_group_changelist')
                )

            if add_group_perm:
                menu.add_modal_item(
                    _('Add new group'),
                    url=admin_reverse('aldryn_people_group_add')
                )

            if change_group_perm and group:
                menu.add_modal_item(
                    _('Edit group'),
                    admin_reverse('aldryn_people_group_change',
                                  args=(group.pk, )),
                    active=True,
                )

            if any(group_perms) and any(person_perms):
                menu.add_break()

            if change_person_perm:
                menu.add_sideframe_item(
                    _('Person list'),
                    url=admin_reverse('aldryn_people_person_changelist')
                )

            if add_person_perm:
                base_url = admin_reverse('aldryn_people_person_add')
                if group:
                    url = "{0}?group={1}".format(base_url, group.pk)
                else:
                    url = base_url
                menu.add_modal_item(_('Add new person'), url=url)

            if change_person_perm and person:
                menu.add_modal_item(
                    _('Edit person'),
                    admin_reverse('aldryn_people_person_change',
                                  args=(person.pk,)),
                    active=True,
                )