# import
from pymatgen.entries.computed_entries import ComputedStructureEntry
from pymatgen.io.ase import AseAtomsAdaptor
from ase.visualize import view
from ocdata.precompute_sample_structures import enumerate_surfaces_for_saving
import json
from ase.io import write

# Opening JSON file
f = open('./ocdata/oc22_dataset/bulk_oxides_20220621.json')

# returns JSON object as a dic
data = json.load(f)
# %%
# load the bulk structures from json file
bulk_db = './ocdata/oc22_dataset/bulk_oxides_20220621.json'
bulk_db_raw_list = [ComputedStructureEntry.from_dict(d) for d in \
                          json.load(open(bulk_db))]
bulk_db_atoms_list = []
for bulk in bulk_db_raw_list:
    bulk_db_atoms_list.append(AseAtomsAdaptor.get_atoms(bulk.structure))
output_folder = './outputs/'
# %% view bulk
print('number of bulks: ', len(bulk_db_atoms_list))
# %% visualization of bulk
bulk_idx = 0
bulk_ase = bulk_db_atoms_list[bulk_idx]
bulk_formula = bulk_ase.symbols.get_chemical_formula()
print('bulk_formula: ', bulk_formula)
# view(bulk_ase)
write(output_folder + 'bulk_'+ bulk_formula +'.eps', bulk_ase)
# %% cut surface
possible_surfaces = enumerate_surfaces_for_saving(bulk_ase)
num_surfaces = len(possible_surfaces)
print('number of surface: ', num_surfaces)
# %% visualization of surfaces

for bulk_idx in range(num_surfaces):
    miller = possible_surfaces[bulk_idx][1]
    shift = possible_surfaces[bulk_idx][2]
    surface_ase = AseAtomsAdaptor.get_atoms(possible_surfaces[bulk_idx][0])
    write(output_folder + 'bulk_' + bulk_formula +'_surface_miller' +str(miller) + '_shift_'+ str(shift)+'.eps', surface_ase)

# %% write to vasp input file
# #%%
# included_surface_indices = range(len(possible_surfaces))
# for cur_surface_ind in included_surface_indices:
#     surface_info = possible_surfaces[cur_surface_ind]
#     surface = Surface(bulk, surface_info, cur_surface_ind, len(possible_surfaces))
#     # job._combine_and_write(surface, self.bulk_indices_list[bulk_ind], cur_surface_ind)
#     # job._write_surface(surface, output_name_template='test_sampling')
#
#
