extern crate embed_resource;

fn main() {
    // Compile versioninfo.rc to embed metadata in the executable
    embed_resource::compile("versioninfo.rc", embed_resource::NONE);
}