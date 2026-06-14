"""AI Art Animator — Main GUI Application (CustomTkinter)."""

from __future__ import annotations
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import shutil
from pathlib import Path
from typing import Optional

from art_animator.core.art_processor import ArtProcessor
from art_animator.core.animator import ArtAnimator
from art_animator.utils.logger import Logger
from art_animator.utils.image_utils import validate_image_path

# UI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_TITLE = "AI Art Animator — Production Studio"
ACCENT = "#4A90E2"
BG_DARK = "#1A1A2E"
BG_MID = "#16213E"
BG_PANEL = "#0F3460"


class AIArtAnimatorApp(ctk.CTk):
    """
    Main GUI application for AI Art Animator.
    
    Provides a professional interface for converting images into
    realistic drawing animations with extensive customization options.
    """

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        # Window setup
        self.title(APP_TITLE)
        self.geometry("1300x820")
        self.configure(fg_color=BG_DARK)
        self.resizable(True, True)
        
        # State
        self.source_image_path: Optional[str] = None
        self.processed_pil: Optional[Image.Image] = None
        self.is_processing: bool = False
        self.animator_output_path: Optional[str] = None
        
        # Core components
        self.logger = Logger(name="GUI")
        self.art_processor = ArtProcessor(logger=self.logger)
        self.animator = ArtAnimator(logger=self.logger)
        self.logger.callback = self.log
        
        # Build UI
        self._build_header()
        self._build_main_area()
        self._build_status_bar()
        
        self.log("✅ AI Art Animator ready. Upload an image to begin.")

    def _build_header(self) -> None:
        """Build application header."""
        h = ctk.CTkFrame(self, height=60, fg_color=BG_PANEL, corner_radius=0)
        h.pack(fill="x", side="top")
        h.pack_propagate(False)
        
        ctk.CTkLabel(
            h, text="🎨  AI Art Animator",
            font=ctk.CTkFont("Segoe UI", 22, weight="bold"),
            text_color=ACCENT
        ).pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(
            h, text="Production Studio  •  Stroke-Level Drawing Simulation",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color="#8899AA"
        ).pack(side="left", padx=10)

    def _build_main_area(self) -> None:
        """Build main content area."""
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)
        main.columnconfigure(0, weight=0, minsize=310)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)
        
        self._build_left_panel(main)
        self._build_right_panel(main)

    def _build_left_panel(self, parent: ctk.CTkFrame) -> None:
        """Build left control panel."""
        left = ctk.CTkScrollableFrame(parent, width=310, fg_color=BG_MID, corner_radius=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Image Upload
        self._sec(left, "📁  Source Image")
        self.upload_btn = ctk.CTkButton(
            left, text="Upload Image", height=40,
            command=self._upload_image,
            fg_color=ACCENT, hover_color="#357ABD",
            font=ctk.CTkFont("Segoe UI", 13, weight="bold")
        )
        self.upload_btn.pack(fill="x", padx=12, pady=(4, 8))

        self.img_label = ctk.CTkLabel(
            left, text="No image loaded", width=280, height=170,
            fg_color="#0A0A1A", corner_radius=8,
            font=ctk.CTkFont("Segoe UI", 11), text_color="#556677"
        )
        self.img_label.pack(padx=12, pady=(0, 12))

        # Art Style
        self._sec(left, "🖌️  Art Style")
        self.style_var = ctk.StringVar(value="Pencil Sketch")
        ctk.CTkOptionMenu(
            left,
            values=["Pencil Sketch", "Advanced Sketch", "Watercolor",
                    "Oil Painting", "Charcoal", "Anime / Manga"],
            variable=self.style_var, height=36,
            fg_color="#1E3A5F", button_color=ACCENT
        ).pack(fill="x", padx=12, pady=(4, 12))

        # Background
        self._sec(left, "📄  Background")
        self.bg_var = ctk.StringVar(value="White Paper")
        ctk.CTkOptionMenu(
            left,
            values=["White Paper", "Aged Paper", "Dark Canvas", "Pure White", "Pure Black"],
            variable=self.bg_var, height=36,
            fg_color="#1E3A5F", button_color=ACCENT
        ).pack(fill="x", padx=12, pady=(4, 12))

        # Resolution
        self._sec(left, "📐  Output Resolution")
        self.res_var = ctk.StringVar(value="1080p (1920×1080)")
        ctk.CTkOptionMenu(
            left,
            values=["720p (1280×720)", "1080p (1920×1080)", "Source Size"],
            variable=self.res_var, height=36,
            fg_color="#1E3A5F", button_color=ACCENT
        ).pack(fill="x", padx=12, pady=(4, 12))

        # Drawing Speed
        self._sec(left, "⚡  Drawing Speed")
        self.speed_val = ctk.CTkLabel(
            left, text="Medium (50)",
            text_color="#AABBCC",
            font=ctk.CTkFont("Segoe UI", 11)
        )
        self.speed_val.pack(anchor="e", padx=14)
        self.speed_slider = ctk.CTkSlider(
            left, from_=1, to=100, number_of_steps=99,
            command=lambda v: self.speed_val.configure(
                text=f"{'Slow' if v<30 else 'Medium' if v<70 else 'Fast'} ({int(v)})"
            ),
            button_color=ACCENT
        )
        self.speed_slider.set(50)
        self.speed_slider.pack(fill="x", padx=12, pady=(2, 12))

        # Detail Level
        self._sec(left, "✏️  Stroke Detail Level")
        self.detail_val = ctk.CTkLabel(
            left, text="High (75)",
            text_color="#AABBCC",
            font=ctk.CTkFont("Segoe UI", 11)
        )
        self.detail_val.pack(anchor="e", padx=14)
        self.detail_slider = ctk.CTkSlider(
            left, from_=10, to=100, number_of_steps=90,
            command=lambda v: self.detail_val.configure(
                text=f"{'Low' if v<35 else 'Medium' if v<65 else 'High'} ({int(v)})"
            ),
            button_color=ACCENT
        )
        self.detail_slider.set(75)
        self.detail_slider.pack(fill="x", padx=12, pady=(2, 12))

        # Shading Intensity
        self._sec(left, "🌑  Shading Intensity")
        self.shade_val = ctk.CTkLabel(
            left, text="60%",
            text_color="#AABBCC",
            font=ctk.CTkFont("Segoe UI", 11)
        )
        self.shade_val.pack(anchor="e", padx=14)
        self.shade_slider = ctk.CTkSlider(
            left, from_=0, to=100, number_of_steps=100,
            command=lambda v: self.shade_val.configure(text=f"{int(v)}%"),
            button_color=ACCENT
        )
        self.shade_slider.set(60)
        self.shade_slider.pack(fill="x", padx=12, pady=(2, 12))

        # FPS
        self._sec(left, "🎞️  Frame Rate")
        self.fps_var = ctk.StringVar(value="30 FPS")
        ctk.CTkOptionMenu(
            left, values=["24 FPS", "30 FPS", "60 FPS"],
            variable=self.fps_var, height=36,
            fg_color="#1E3A5F", button_color=ACCENT
        ).pack(fill="x", padx=12, pady=(4, 12))

        # Extra Options
        self._sec(left, "⚙️  Extra Options")
        self.paper_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            left, text="Paper Texture Overlay",
            variable=self.paper_var,
            text_color="#CCDDEE"
        ).pack(anchor="w", padx=14, pady=3)

        self.jitter_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            left, text="Human Stroke Jitter",
            variable=self.jitter_var,
            text_color="#CCDDEE"
        ).pack(anchor="w", padx=14, pady=3)

        self.timelapse_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            left, text="Time-lapse Mode",
            variable=self.timelapse_var,
            text_color="#CCDDEE"
        ).pack(anchor="w", padx=14, pady=3)

        self.gif_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            left, text="Also Export GIF",
            variable=self.gif_var,
            text_color="#CCDDEE"
        ).pack(anchor="w", padx=14, pady=(3, 14))

        # Action Buttons
        self.process_btn = ctk.CTkButton(
            left, text="🖌  Generate Art", height=44,
            command=self._start_processing,
            fg_color="#2ECC71", hover_color="#27AE60",
            font=ctk.CTkFont("Segoe UI", 14, weight="bold"),
            state="disabled"
        )
        self.process_btn.pack(fill="x", padx=12, pady=(6, 6))

        self.animate_btn = ctk.CTkButton(
            left, text="🎬  Create Animation", height=44,
            command=self._start_animation,
            fg_color="#9B59B6", hover_color="#7D3C98",
            font=ctk.CTkFont("Segoe UI", 14, weight="bold"),
            state="disabled"
        )
        self.animate_btn.pack(fill="x", padx=12, pady=(0, 6))

        self.export_btn = ctk.CTkButton(
            left, text="💾  Export MP4", height=44,
            command=self._export_video,
            fg_color="#E67E22", hover_color="#CA6F1E",
            font=ctk.CTkFont("Segoe UI", 14, weight="bold"),
            state="disabled"
        )
        self.export_btn.pack(fill="x", padx=12, pady=(0, 14))

    def _build_right_panel(self, parent: ctk.CTkFrame) -> None:
        """Build right preview and console panel."""
        right = ctk.CTkFrame(parent, fg_color=BG_MID, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=3)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Preview
        preview_frame = ctk.CTkFrame(right, fg_color="#0A0A1A", corner_radius=10)
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=14, pady=(14, 8))
        
        ctk.CTkLabel(
            preview_frame, text="PREVIEW",
            font=ctk.CTkFont("Segoe UI", 10, weight="bold"),
            text_color="#334455"
        ).pack(anchor="nw", padx=10, pady=(6, 0))
        
        self.preview_canvas = ctk.CTkLabel(
            preview_frame, text="", fg_color="#0A0A1A", corner_radius=0
        )
        self.preview_canvas.pack(fill="both", expand=True, padx=6, pady=6)
        
        self.ph_label = ctk.CTkLabel(
            preview_frame, text="Upload an image to see preview",
            font=ctk.CTkFont("Segoe UI", 14), text_color="#334455"
        )
        self.ph_label.place(relx=0.5, rely=0.5, anchor="center")

        # Progress + Console
        bottom = ctk.CTkFrame(right, fg_color="transparent")
        bottom.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        bottom.rowconfigure(2, weight=1)
        bottom.columnconfigure(0, weight=1)

        pr = ctk.CTkFrame(bottom, fg_color="transparent")
        pr.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        pr.columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(
            pr, height=16, progress_color=ACCENT, fg_color="#0A0A1A"
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            pr, text="Idle", font=ctk.CTkFont("Segoe UI", 11),
            text_color="#7788AA", width=140
        )
        self.progress_label.grid(row=0, column=1, padx=(10, 0))

        ctk.CTkLabel(
            bottom, text="STATUS LOG",
            font=ctk.CTkFont("Segoe UI", 10, weight="bold"),
            text_color="#334455"
        ).grid(row=1, column=0, sticky="w")
        
        self.console = ctk.CTkTextbox(
            bottom, height=130, fg_color="#050510",
            text_color="#00FF88", font=ctk.CTkFont("Consolas", 11), corner_radius=6
        )
        self.console.grid(row=2, column=0, sticky="nsew")

    def _build_status_bar(self) -> None:
        """Build bottom status bar."""
        bar = ctk.CTkFrame(self, height=28, fg_color="#0A0A1A", corner_radius=0)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            bar, text="Ready", font=ctk.CTkFont("Segoe UI", 10), text_color="#556677"
        )
        self.status_label.pack(side="left", padx=14)

    def _sec(self, parent: ctk.CTkFrame, text: str) -> None:
        """Render a section label."""
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
            text_color=ACCENT, anchor="w"
        ).pack(fill="x", padx=12, pady=(10, 2))

    def log(self, msg: str) -> None:
        """Thread-safe console log."""
        self.after(0, self._log_safe, msg)

    def _log_safe(self, msg: str) -> None:
        """Internal log handler (must run on main thread)."""
        self.console.configure(state="normal")
        self.console.insert("end", msg + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")
        self.status_label.configure(text=msg[:90])

    def set_progress(self, value: float, label: str = "") -> None:
        """Update progress bar (thread-safe)."""
        self.after(0, lambda: (
            self.progress_bar.set(value),
            self.progress_label.configure(text=label or f"{int(value * 100)}%")
        ))

    def _update_preview(self, pil_img: Image.Image) -> None:
        """Update preview image (thread-safe)."""
        self.after(0, self._show_preview, pil_img)

    def _show_preview(self, pil_img: Image.Image) -> None:
        """Internal preview handler (must run on main thread)."""
        w = self.preview_canvas.winfo_width() or 700
        h = self.preview_canvas.winfo_height() or 420
        if w < 50:
            w, h = 700, 420
        
        img = pil_img.copy()
        img.thumbnail((w - 12, h - 12), Image.LANCZOS)
        self._tk_img = ImageTk.PhotoImage(img)
        self.preview_canvas.configure(image=self._tk_img, text="")
        
        try:
            self.ph_label.place_forget()
        except:
            pass

    def _upload_image(self) -> None:
        """Handle image upload."""
        path = filedialog.askopenfilename(
            title="Select Source Image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"), ("All", "*.*")]
        )
        if not path:
            return
        
        ok, msg = validate_image_path(path)
        if not ok:
            messagebox.showerror("Invalid Image", msg)
            return
        
        self.source_image_path = path
        pil = Image.open(path).convert("RGB")
        
        # Thumbnail
        thumb = pil.copy()
        thumb.thumbnail((280, 170), Image.LANCZOS)
        self._thumb_tk = ImageTk.PhotoImage(thumb)
        self.img_label.configure(image=self._thumb_tk, text="")
        
        # Preview
        self._update_preview(pil)
        
        # Update UI state
        self.process_btn.configure(state="normal")
        self.export_btn.configure(state="disabled")
        self.animate_btn.configure(state="disabled")
        self.processed_pil = None
        
        self.log(f"📂 Loaded: {Path(path).name}  ({pil.width}×{pil.height})")

    def _start_processing(self) -> None:
        """Start art style processing in background thread."""
        if not self.source_image_path or self.is_processing:
            return
        
        self.is_processing = True
        self.process_btn.configure(state="disabled")
        self.animate_btn.configure(state="disabled")
        threading.Thread(target=self._run_processing, daemon=True).start()

    def _run_processing(self) -> None:
        """Run art style processing (background thread)."""
        try:
            style = self.style_var.get()
            shade = self.shade_slider.get() / 100.0
            
            self.log(f"🎨 Applying style: {style} ...")
            self.set_progress(0.1, "Processing...")
            
            result = self.art_processor.apply_style(
                image_path=self.source_image_path,
                style=style,
                shading_intensity=shade,
                progress_cb=self.set_progress
            )
            
            self.processed_pil = result
            self._update_preview(result)
            self.set_progress(1.0, "Art ready!")
            self.log("✅ Style applied successfully.")
            
            self.after(0, lambda: (
                self.animate_btn.configure(state="normal"),
                self.process_btn.configure(state="normal")
            ))
        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.set_progress(0, "Error")
            self.after(0, lambda: self.process_btn.configure(state="normal"))
        finally:
            self.is_processing = False

    def _start_animation(self) -> None:
        """Start animation creation in background thread."""
        if self.processed_pil is None or self.is_processing:
            return
        
        self.is_processing = True
        self.animate_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        threading.Thread(target=self._run_animation, daemon=True).start()

    def _run_animation(self) -> None:
        """Run animation creation (background thread)."""
        try:
            res_map = {
                "720p (1280×720)": (1280, 720),
                "1080p (1920×1080)": (1920, 1080),
                "Source Size": None,
            }
            fps_map = {"24 FPS": 24, "30 FPS": 30, "60 FPS": 60}
            
            self.log("🎬 Building drawing animation...")
            self.set_progress(0.05, "Analyzing strokes...")
            
            out = self.animator.create_animation(
                styled_image=self.processed_pil,
                source_path=self.source_image_path,
                style=self.style_var.get(),
                speed=int(self.speed_slider.get()),
                detail_level=int(self.detail_slider.get()),
                fps=fps_map.get(self.fps_var.get(), 30),
                resolution=res_map.get(self.res_var.get()),
                paper_texture=self.paper_var.get(),
                human_jitter=self.jitter_var.get(),
                timelapse=self.timelapse_var.get(),
                export_gif=self.gif_var.get(),
                bg_type=self.bg_var.get(),
                progress_cb=self.set_progress,
                preview_cb=self._update_preview,
            )
            
            self.animator_output_path = out
            self.log(f"✅ Animation saved: {out}")
            self.set_progress(1.0, "Done!")
            
            self.after(0, lambda: (
                self.export_btn.configure(state="normal"),
                self.animate_btn.configure(state="normal")
            ))
        except Exception as e:
            import traceback
            self.log(f"❌ Error: {e}")
            self.log(traceback.format_exc())
            self.set_progress(0, "Error")
            self.after(0, lambda: self.animate_btn.configure(state="normal"))
        finally:
            self.is_processing = False

    def _export_video(self) -> None:
        """Export video to user-selected location."""
        if not self.animator_output_path:
            return
        
        dest = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")],
            title="Export Animation"
        )
        
        if dest:
            shutil.copy2(self.animator_output_path, dest)
            self.log(f"💾 Exported to: {dest}")
            messagebox.showinfo("Export Complete", f"Animation saved to:\n{dest}")


def launch() -> None:
    """Launch the GUI application."""
    app = AIArtAnimatorApp()
    app.mainloop()


if __name__ == "__main__":
    launch()
