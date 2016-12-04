from django.apps import apps as django_apps

from edc_identifier.models import IdentifierModel

edc_device_app_config = django_apps.get_app_config('edc_device')


class InfantIdentifierError(Exception):
    pass


class InfantIdentifier:
    def __init__(self, model=None, maternal_identifier=None, birth_order=None,
                 live_infants=None, template=None):
        subject_type = 'infant'
        template = template or '{maternal_identifier}-{infant_suffix}'
        try:
            maternal_identifier = IdentifierModel.objects.get(identifier=maternal_identifier)
        except IdentifierModel.DoesNotExist:
            raise InfantIdentifierError(
                'Unable to allocate infant identifier. Maternal_identifier {0} does not exist.'.format(
                    maternal_identifier))
        if birth_order > live_infants:
            raise InfantIdentifierError(
                'Unable to allocate infant identifier. Birth order cannot be {} '
                'if number of live infants is {}.'.format(birth_order, live_infants))
        if live_infants == 1:
            infant_suffix = 10  # singlet 10
        elif live_infants == 2:
            infant_suffix = 25  # twins 25,26
        elif live_infants == 3:
            infant_suffix = 36  # triplets 36,37,38
        elif live_infants == 4:
            infant_suffix = 47  # quadruplets 47,48,49,50
        elif live_infants == 5:
            infant_suffix = 58  # qintplets 58, 59, 60, 61, 62
        else:
            raise InfantIdentifierError(
                'Unable to allocate infant identifier. Ensure number of infants is greater than 0 and less than '
                'or equal to 5. You wrote %s' % (live_infants))
        infant_suffix += birth_order
        self.identifier = template.format(
            maternal_identifier=maternal_identifier.identifier,
            infant_suffix=infant_suffix)
        IdentifierModel.objects.create(
            name=self.name,
            sequence_number=infant_suffix,
            identifier=self.identifier,
            protocol_number=maternal_identifier.protocol_number,
            device_id=edc_device_app_config.device_id,
            model=model,
            study_site=maternal_identifier.study_site,
            subject_type=subject_type)

    @property
    def name(self):
        return 'infantidentifier'