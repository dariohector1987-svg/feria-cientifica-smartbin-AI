// ===== Datos editables =====
const VIDEO_ID = "";   // ID del video de YouTube (lo que va después de v= en el enlace)
const EMAIL = "";      // Correo que recibirá los mensajes del formulario

document.addEventListener("DOMContentLoaded", () => {
  const anio = document.getElementById("anio");
  if (anio) anio.textContent = new Date().getFullYear();

  const video = document.getElementById("video");
  if (video) {
    video.innerHTML = VIDEO_ID
      ? `<iframe src="https://www.youtube.com/embed/${VIDEO_ID}" title="Video demostrativo de SmartBin AI" allowfullscreen></iframe>`
      : "<p>🎬 El video demostrativo se publicará próximamente.</p>";
  }

  const codigo = document.getElementById("codigo");
  if (codigo) {
    fetch("smartbin.py").then(r => r.text()).then(t => { codigo.textContent = t; })
      .catch(() => { codigo.textContent = "No se pudo cargar smartbin.py"; });
  }

  const form = document.getElementById("form-contacto");
  if (form) {
    form.addEventListener("submit", e => {
      e.preventDefault();
      const msg = document.getElementById("estado-form");
      if (!EMAIL) { msg.textContent = "El correo de contacto aún no está configurado."; return; }
      const d = new FormData(form);
      const asunto = encodeURIComponent("Contacto SmartBin AI - " + d.get("nombre"));
      const cuerpo = encodeURIComponent(d.get("mensaje") + "\n\nDe: " + d.get("nombre") + " (" + d.get("correo") + ")");
      window.location.href = `mailto:${EMAIL}?subject=${asunto}&body=${cuerpo}`;
      msg.textContent = "Se abrirá tu aplicación de correo para enviar el mensaje.";
    });
  }
});
