from django.conf.urls import url
from django.utils import timezone
from dashboard.models import Equipment, User, Usage
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from tastypie.utils.timezone import now

import json


class EquipmentResource(ModelResource):
    class Meta:
        queryset = Equipment.objects.all()
        equipment_resource = 'equipment'
        user_resource = 'user'
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<equipment_resource>%s)/equip%s$" %
                (self._meta.equipment_resource, trailing_slash()),
                self.wrap_view('get_equipment'), name='api_get_equipment'),
            url(r"^(?P<equipment_resource>%s)/switch%s$" %
                (self._meta.equipment_resource, trailing_slash()),
                self.wrap_view('toggle_equipment'), name='api_toggle_equipment'),
            url(r"^(?P<user_resource>%s)/login%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('validate_user'), name='api_validate_user')
        ]

    def validate_key(self, body, key):
        if not body:
            result = {'status':False, 'message': f'Expected equipment {key}'}
        equipment = Equipment.objects.filter(id=body[key])
        if equipment.count() < 1:
            result = {'status':False, 'message': f'Equipment {key} does not exist'}
        return {'status': True, 'query': equipment[0]}

    def get_equipment(self, request, *args, **kwargs):
        body = json.loads(request.body)
        result = self.validate_key(body, 'id')
        if not result['status']:
            return self.create_response(request, result)
        equipment = result['query']
        response = {
            'name': equipment.name,
            'rating': equipment.rating,
            'priority': equipment.priority
        }
        return self.create_response(request, response)

    def toggle_equipment(self, request, *args, **kwargs):
        # equip_id, status
        body = json.loads(request.body)
        result = self.validate_key(body, 'id')
        if not result['status']:
            return self.create_response(request, result)
        equipment = result['query']
        equipment_usage = Usage.objects.filter(equipment=equipment)
        if equipment_usage.count() < 1:
            result = {'status':False, 'message': f'{equipment.name}\'s usage does not exist'}
            return self.create_response(request, result)
        equipment_usage = equipment_usage[0]
        required_state = body.get('state')
        if equipment_usage.state and required_state:
            pass
        if not equipment_usage.state and not required_state:
            pass
        if not equipment_usage.state and required_state:
            equipment_usage.state = required_state
            equipment_usage.started_at = timezone.now()
            equipment_usage.save()
            # toggle gpio switch
        if equipment_usage.state and not required_state:
            equipment_usage.state = required_state
            equipment_usage.started_at = timezone.now()
            equipment_usage.save()
            # toggle gpio switch
        result = {
            'name': equipment.name,
            'state': equipment_usage.state,
            'time': equipment_usage.started_at
        }
        return self.create_response(request, result)

    def validate_user(self, request, *args, **kwargs):
        body = json.loads(request.body)
        # think about good authentication module
        result = {'status': True, 'body': body}
        return self.create_response(request, result)