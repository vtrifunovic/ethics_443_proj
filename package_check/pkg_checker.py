from importlib.metadata import metadata, requires
import os
import stat
import re
from checker_utils.pycolors import printc

class PkgCheck:
    def __init__(self):
        self.pkg_dict = {}
        self.valid_lic = {}
        self.scan_files = []
        self.deps = {}

    def _dep_scan(self, pkg_name, file_name):
        try:
            for i in requires(pkg_name):
                dep_name = i.split(";")[0]
                dep_name = dep_name.split(">")[0]
                dep_name = dep_name.split("<")[0]
                dep_name = dep_name.split("=")[0]
                dep_name = dep_name.split(" ")[0].strip()
                if dep_name not in self.deps and dep_name not in self.pkg_dict:
                    self.deps[dep_name] = [pkg_name, file_name.split("/")[-1]]
                    #self._dep_scan(dep_name, file_name)
        except Exception as e:
            #print(e)
            return
        
    def _scan_import(self, pkg_name, file_name=None):
        try:
            meta = metadata(pkg_name)
        except:
            return None
        if file_name:
            self._dep_scan(pkg_name, file_name)
        if "License" in meta:
            for line in meta['License'].split("\n"):
                if line.lower().startswith("license:"):
                    return re.sub("license:", "", line, flags=re.I).strip()
                
            for line in meta['License'].split("\n"):
                if len(line) < 1:
                    continue
                if line[0].isalpha():
                    return line.strip()
        return None
    
    def _clean_pkgs(self):
        for k, v in self.pkg_dict.items():
            if v[0]:
                self.valid_lic[k] = v

    def _open_python_file(self, file_name, deep):
        f = open(file_name, "r").readlines()
        print("Checking:", end=" ")
        printc(file_name, fore="green")
        for line in f:
            if line.startswith('import') or line.startswith('from'):
                pkg = line.split(" ")[1].split(".")[0].strip()
                if pkg in self.pkg_dict:
                    continue
                self.pkg_dict[pkg] = [self._scan_import(pkg, file_name), file_name.split("/")[-1]]
        
        if deep:
            for dep, v in self.deps.items():
                if dep in self.pkg_dict:
                    continue
                self.pkg_dict[dep] = [self._scan_import(dep), v[1], v[0]] # fix

        self._clean_pkgs()       

    def _scan_directory(self, dir):
        all_files = os.listdir(dir)
        for f in all_files:
            self._get_scan_files(os.path.join(dir, f))

    def _get_scan_files(self, dir):
        stat_info = os.stat(dir)
        if stat.S_ISDIR(stat_info.st_mode):
            self._scan_directory(dir)
        elif stat.S_ISREG(stat_info.st_mode):
            self.scan_files.append(dir)

    def scan_project(self, dir, deep=True):
        self._get_scan_files(dir)
        for i in self.scan_files:
            if i.endswith(".py"):
                self._open_python_file(i, deep)

    def analyze_licenses(self, license_list):
        issues = 0
        license_list = [fr"\b{i}\b" for i in license_list]
        for k, v in self.valid_lic.items():
            if not v[0]: # safe tea check
                continue
            for lic in license_list:
                if re.findall(lic, v[0]):
                    issues += 1
                    print(f"Issue found:", end=" ")
                    printc(k, fore="red")
                    print(f"\tUses license: {v[0]}") 
                    print("\tImported by file: ", end="")
                    printc(v[1], fore="black", back="yellow")
        if issues == 0:
            printc("No issues found!", fore="green")
            return
        print("Total of", end=" ")
        printc(issues, fore="red", end=" ")
        print("issues found. ")


    def list_all(self, found=True):
        curr_dic = self.valid_lic
        if not found:
            curr_dic = self.pkg_dict
        if not curr_dic:
            return
        max_len = max([len(l) for l in curr_dic])+1
        for k, v in curr_dic.items():
            printc(k.strip(), fore="cyan", end=" "*(max_len-len(k.strip())))
            print(v[0])


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to project")
    parser.add_argument("--avoid", required=True, help="List of lisences to avoid, separated by commas")
    parser.add_argument("--deep", action="store_true", required=False, help="Check dependencies")
    parser.add_argument("--noanalysis", action="store_true", required=False, help="Skip analysis")
    parser.add_argument("--listall", action="store_true", required=False, help="List all licenses found")
    parser.add_argument("--all", action="store_true", required=False, help="When used with 'listall', will list all packages even ones without licenses")
    args = parser.parse_args()

    ck = PkgCheck()
    ck.scan_project(args.path, deep=args.deep)
    args.avoid = [i.strip() for i in args.avoid.split(",")]
    if not args.noanalysis:
        input("Analysis")
        ck.analyze_licenses(license_list=args.avoid)
    if args.listall:
        input("List all")
        ck.list_all(found=not args.all)