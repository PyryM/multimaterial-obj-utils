import argparse
import objparse

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Split a multimaterial obj')
    p.add_argument('source', help='source .obj file')
    p.add_argument('dest', help='destination prefix')
    args = p.parse_args()

    with open(args.source, "rt") as src:
        srcdata = objparse.parse_obj(src)
    for mtl in srcdata['face_sets'].keys():
        subdata = objparse.gen_submaterial_obj(srcdata, mtl)
        with open("{}_{}.obj".format(args.dest, mtl), "wt") as dest:
            objparse.write_obj(dest, subdata)
