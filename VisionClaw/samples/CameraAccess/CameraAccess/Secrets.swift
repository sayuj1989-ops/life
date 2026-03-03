// VisionClaw Secrets Configuration
// Fill in your values below, OR configure them at runtime in the app's Settings screen.
//
// NOTE: Your Gemini API key is already saved on your phone from the previous build.
// You only need to fill in the OpenClaw section below.

import Foundation

enum Secrets {
  // REQUIRED: Get your key at https://aistudio.google.com/apikey
  // (Already set on your phone from previous app — leave this as-is)
  static let geminiAPIKey = "YOUR_GEMINI_API_KEY"

  // ── OpenClaw Setup ─────────────────────────────────────────────
  // Enables agentic tool-calling: send messages, web search, lists, etc.
  //
  // Step 1: Find your Mac's hostname
  //   Run in Terminal: scutil --get LocalHostName
  //   Or: System Settings > General > Sharing (shown at top)
  //   Example: "Johns-MacBook-Pro"
  //
  // Step 2: Find your gateway token
  //   Run in Terminal: cat ~/.openclaw/openclaw.json
  //   Look for: "gateway" > "auth" > "token"
  //
  // Step 3: Fill in below (or use the in-app Settings screen)
  //
  // Host format: "http://YOUR-HOSTNAME.local" (with or without http://)
  static let openClawHost = "http://YOUR_MAC_HOSTNAME.local"
  static let openClawPort = 18789
  static let openClawHookToken = "YOUR_OPENCLAW_HOOK_TOKEN"
  static let openClawGatewayToken = "YOUR_OPENCLAW_GATEWAY_TOKEN"

  // OPTIONAL: WebRTC signaling server URL (for live POV streaming)
  static let webrtcSignalingURL = "ws://YOUR_MAC_IP:8080"
}
