"use client";

import { useEffect } from "react";

export function ServiceWorkerRegister() {
  useEffect(() => {
    if (!("serviceWorker" in navigator)) return;

    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
      navigator.serviceWorker.getRegistrations().then((regs) => {
        for (const r of regs) {
          r.unregister();
        }
      });
    } else {
      const registerSW = () => {
        navigator.serviceWorker
          .register("/sw.js", { scope: "/" })
          .catch((err) => {
            console.error("Poth SW registration error: ", err);
          });
      };

      if (document.readyState === "complete" || document.readyState === "interactive") {
        registerSW();
      } else {
        window.addEventListener("load", registerSW, { once: true });
      }
    }
  }, []);

  return null;
}
