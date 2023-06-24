import yaml
from extras.scripts import Script, ObjectVar
from core.models import DataSource, DataFile
from dcim.models import Site


class LoadDataSourceScript(Script):
    class Meta:
        name = 'Load Data Source'
        description = 'Load NetBox Data from Data Source'
        field_order = ['data_source', 'data_file']

    data_source = ObjectVar(
        model=DataSource,
        required=True
    )

    data_file = ObjectVar(
        model=DataFile,
        required=True,
        query_params={
            'source_id': '$data_source'
        }
    )

    def run(self, data, commit):
        try:
            load_data = yaml.safe_load(data['data_file'].data_as_string)
        except:
            self.log_failure('load data is not invalid yaml')
            return

        if not isinstance(load_data, dict):
            self.log_failure('load data is not dict')
            return

        if 'sites' in load_data:
            sites = load_data['sites']

            for site in sites:
                n_site, created = Site.objects.get_or_create(
                    name=site['name'],
                    slug=site['slug'],
                    status=site['status']
                )
                self.log_success(f'{"Create" if created else "Update"} site: {n_site}')

        return
