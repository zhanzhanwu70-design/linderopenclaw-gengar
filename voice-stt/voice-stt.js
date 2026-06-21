#!/usr/bin/env node
/**
 * voice-stt.js - Transcribe OGG audio files using local whisper.cpp (napi-rs)
 * 
 * Usage: node voice-stt.js <audio-file.ogg>
 * 
 * Output: Plain text transcript to stdout
 * 
 * Model: ggml-base.en (downloaded to ~/.whisper-models/)
 * Language: English (optimized)
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { Whisper, WhisperFullParams, WhisperSamplingStrategy } from '@napi-rs/whisper';
import audioDecode from 'audio-decode';

const MODEL_PATH = join(process.env.HOME || '/home/node', '.whisper-models', 'ggml-base.en.bin');
const INPUT_FILE = process.argv[2] || '';

if (!INPUT_FILE) {
  console.error('Usage: node voice-stt.js <audio-file.ogg>');
  process.exit(1);
}

if (!existsSync(INPUT_FILE)) {
  console.error(`File not found: ${INPUT_FILE}`);
  process.exit(1);
}

if (!existsSync(MODEL_PATH)) {
  console.error(`Model not found at ${MODEL_PATH}`);
  console.error('Download with: node /path/to/@napi-rs/whisper/scripts/download-ggml-model.mjs base.en ~/.whisper-models/');
  process.exit(1);
}

try {
  const model = readFileSync(MODEL_PATH);
  const audio = readFileSync(INPUT_FILE);
  const wav = await audioDecode(audio);
  const mono = wav.channelData[0];

  const whisper = new Whisper(model);
  const params = new WhisperFullParams(WhisperSamplingStrategy.Greedy);
  params.language = 'en';
  params.singleSegment = true;
  params.durationMs = 0;

  const output = whisper.full(params, mono);
  const text = output.text || output[0]?.text || String(output);

  process.stdout.write(String(text).trim());
} catch (err) {
  console.error('Transcription error:', err.message);
  process.exit(1);
}