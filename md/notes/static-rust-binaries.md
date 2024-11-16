
### **Building Fully Static Rust Binaries for Multiple Architectures**

This guide demonstrates how to build Rust binaries for different architectures using Musl in an isolated Alpine-based container.

#### **Step 1: Build and Run the Container**

From the root of the repository:

1. **Build the Docker image:**
   ```bash
   docker build -t musl-rust-build -f docker/Dockerfile.xcompile .
   ```

2. **Run the container:**
   ```bash
   docker run -it --rm -v "$(pwd):/workspace" musl-rust-build
   ```

---

### **Step 2: Configure Cross-Compilation Targets**
Inside the container:
1. **Install Cross-Compilation Targets:**
   Rust supports multiple architectures via `rustup`. Install the desired targets:
   ```bash
   rustup target add \
       aarch64-unknown-linux-musl \
       x86_64-unknown-linux-musl \
       armv7-unknown-linux-musleabihf \
       i686-unknown-linux-musl
   ```

2. **Verify Installed Targets:**
   List the installed targets:
   ```bash
   rustup show
   ```

---

### **Step 3: Build for Specific Architectures**
1. **Navigate to the Project Directory:**
   ```bash
   cd /workspace/rs
   ```

2. **Build for Supported Architectures:**
   Run `cargo build` with the `--target` option:

```bash
cargo build --release --target aarch64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
cargo build --release --target armv7-unknown-linux-musleabihf
cargo build --release --target i686-unknown-linux-musl
```

---

### **Step 4: Verify and Collect the Binaries**
1. **Find the Binaries:**
   The binaries are stored in `target/<architecture>/release/`. Example:
   ```bash
   ls target/aarch64-unknown-linux-musl/release/
   ```

2. **Check Binary Type:**
   Use `file` to confirm the binary is for the correct architecture:
   ```bash
   file target/aarch64-unknown-linux-musl/release/corpora_cli
   ```

3. **Confirm Static Linking:**
   Use `ldd` to ensure the binary is static:
   ```bash
   ldd target/aarch64-unknown-linux-musl/release/corpora_cli
   ```
   The output should say:
   ```
   not a dynamic executable
   ```

---

### **Supported Architectures**
Here are common Musl-compatible architectures you can target:

| Architecture                      | Rust Target                     | Notes                                 |
|-----------------------------------|----------------------------------|---------------------------------------|
| ARM 64-bit                        | `aarch64-unknown-linux-musl`    | Modern 64-bit ARM platforms           |
| ARM 32-bit (hard float)           | `armv7-unknown-linux-musleabihf`| Older ARM platforms with hardware FPU |
| x86 64-bit                        | `x86_64-unknown-linux-musl`     | Standard 64-bit Intel/AMD             |
| x86 32-bit                        | `i686-unknown-linux-musl`       | Legacy 32-bit Intel/AMD               |

---

### **Step 5: Deploy the Binaries**
You can now copy these binaries to your deployment environment. For example:
- Use `scp` to transfer the binary to a remote server.
- Serve the binary over HTTP using a debug Django view (e.g., `/bin/<arch>/`).

---

### **Tips for Extending the Workflow**
- **Custom Build Options:**
  Use `RUSTFLAGS` to tweak optimization or static linking behavior:
  ```bash
  RUSTFLAGS="-C target-feature=+crt-static" cargo build --release --target <arch>
  ```

- **Add Additional Architectures:**
  Check Rust's supported targets:
  ```bash
  rustup show all
  ```
  Add more Musl-compatible targets as needed.
