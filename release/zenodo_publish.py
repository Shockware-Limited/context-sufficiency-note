"""Create (and optionally publish) a Zenodo deposition for the note.

Usage:
  python zenodo_publish.py --host sandbox.zenodo.org --token-file ~/.config/context-sufficiency-note/zenodo-token-2 \
      --pdf ../paper/main.pdf --metadata zenodo-metadata.json [--extra ../sufficiency/Sufficiency/NonMonotonic.lean ...] [--publish]

Without --publish it creates an unsubmitted draft, uploads the files, applies the metadata, and prints
the reserved DOI and the draft URL. With --publish it also publishes (irreversible on production).
"""
import argparse, json, os, sys, urllib.request, urllib.error

def req(method, url, token, data=None, content_type="application/json", raw=False):
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None and not raw:
        data = json.dumps(data).encode("utf-8"); headers["Content-Type"] = content_type
    # raw bucket uploads: Zenodo rejects an explicit Content-Type with 415; send none.
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:500]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True); ap.add_argument("--token-file", required=True)
    ap.add_argument("--pdf", required=True); ap.add_argument("--metadata", required=True)
    ap.add_argument("--extra", nargs="*", default=[]); ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    token = open(os.path.expanduser(a.token_file), encoding="utf-8").read().strip()
    H = f"https://{a.host}/api"
    st, dep = req("POST", f"{H}/deposit/depositions", token, data={})
    if st != 201: sys.exit(f"create failed {st}: {dep}")
    did = dep["id"]; bucket = dep["links"]["bucket"]
    print(f"deposition {did} on {a.host}")
    for path in [a.pdf] + a.extra:
        name = os.path.basename(path)
        with open(path, "rb") as fh:
            st, r = req("PUT", f"{bucket}/{name}", token, data=fh.read(), content_type="application/octet-stream", raw=True)
        print(f"  upload {name}: {st}")
        if st not in (200, 201): sys.exit("upload failed")
    meta = json.load(open(a.metadata, encoding="utf-8"))
    st, r = req("PUT", f"{H}/deposit/depositions/{did}", token, data=meta)
    if st != 200: sys.exit(f"metadata failed {st}: {r}")
    doi = r["metadata"].get("prereserve_doi", {}).get("doi")
    print(f"  metadata ok; reserved DOI: {doi}")
    print(f"  draft: {r['links'].get('html')}")
    if a.publish:
        st, r = req("POST", f"{H}/deposit/depositions/{did}/actions/publish", token, data={})
        if st != 202: sys.exit(f"publish failed {st}: {r}")
        print(f"PUBLISHED: doi={r.get('doi')} record={r['links'].get('record_html')}")
    else:
        print("draft left unpublished")

if __name__ == "__main__":
    main()
