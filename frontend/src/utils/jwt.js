// src/utils/jwt.js
export function parseJwt(token) {
  // token = header.payload.signature
  const payload = token.split('.')[1]
  // atob decodes base64 → string
  const json    = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
  return JSON.parse(json)
}
