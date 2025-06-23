// src/api/chat.js
import api from './axios';

export function sendQuestion(sessionId, question) {
  return api.post('/chat', { session_id: sessionId, question });
}
