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
        sites = yaml.safe_load(self.data_file.data_as_string)
        output = []

        for site in sites:
            n_site = Site(
                name=data['name'],
                slug=data['slug'],
                status=data['status']
            )
            n_site.full_clean()
            n_site.save()
            self.log_success(f"Created new site: {n_site}")
            output.append(f'{n_site.name}')
        return '\n'.join(output)
