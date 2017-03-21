# parses an obj file
def _parse_attr_raw(line, gps, data):
    # don't parse the line into actual components, just store the raw string
    data[gps[0]].append(line)

def _parse_face_raw(line, gps, data):
    if not data['curmtl'] in data['face_sets']:
        data['face_sets'][data['curmtl']] = []
    data['face_sets'][data['curmtl']].append(line)

def _change_material(line, gps, data):
    data['curmtl'] = gps[1]

def _parse_mtllib(line, gps, data):
    data['mtllibs'].append(line)

def parse_obj(src):
    data = {'v': [], 'vt': [], 'vn': [], 'face_sets': {}, 'curmtl': 'none',
            'mtllibs': []}
    parsers = {'v': _parse_attr_raw, 'vt': _parse_attr_raw,
               'vn': _parse_attr_raw, 'f': _parse_face_raw,
               'usemtl': _change_material, 'mtllib': _parse_mtllib}

    num_unparsed = 0

    for line in src:
        gps = line.strip().split(" ")
        if len(gps) < 2:
            continue
        if gps[0] in parsers:
            parsers[gps[0]](line, gps, data)
        else:
            num_unparsed += 1

    print("num unparsed lines: {}".format(num_unparsed))
    return data

_attr_keys = ['v', 'vt', 'vn']
def write_obj(dest, data):
    for mtlline in data['mtllibs']:
        dest.write(mtlline)
    for attr in _attr_keys:
        for attrline in data[attr]:
            dest.write(attrline)
    # note: inefficient in python2
    for (mtlname, mtlfaces) in data['face_sets'].items():
        dest.write('usemtl {}\n'.format(mtlname))
        for faceline in mtlfaces:
            dest.write(faceline)

def _reindex_vertex(v, srcdata, newdata, indextables):
    subgps = v.split("/")
    newindices = []
    for (idx, attr) in zip(subgps, _attr_keys):
        if idx == '':
            newindices.append('')
        else:
            idx = int(idx)
            if idx in indextables[attr]:
                newindices.append(str(indextables[attr][idx]))
            else:
                # objs are 1 indexed
                newdata[attr].append(srcdata[attr][idx-1])
                newidx = len(newdata[attr])
                indextables[attr][idx] = newidx
                newindices.append(str(newidx))
    return "/".join(newindices)

def _append_reindexed_face(faceline, srcdata, newdata, indextables):
    gps = faceline.strip().split()
    verts = [_reindex_vertex(g, srcdata, newdata, indextables) for g in gps[1:]]
    newfaceline = "f {}\n".format(" ".join(verts))
    newdata['face_sets'][newdata['curmtl']].append(newfaceline)

def gen_submaterial_obj(data, material_name):
    if not material_name in data['face_sets']:
        print("No face set for {}".format(material_name))
        return

    newdata = {'v': [], 'vt': [], 'vn': [], 'face_sets': {},
               'curmtl': material_name, 'mtllibs': data['mtllibs']}
    newdata['face_sets'][material_name] = []
    reeindex_tables = {'v': {}, 'vt': {}, 'vn': {}}

    for faceline in data['face_sets'][material_name]:
        _append_reindexed_face(faceline, data, newdata, reeindex_tables)

    return newdata
