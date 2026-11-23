import os
import sys
import json
import argparse
import urllib.request
import urllib.error

API_URL = 'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'


def synthesize(text, voice_id, api_key, model_id, out_path):
    url = API_URL.format(voice_id=voice_id)
    payload = json.dumps({
        'text': text,
        'model_id': model_id,
        'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}
    }).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        method='POST',
        headers={
            'xi-api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'audio/mpeg',
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            audio = resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        print(f'HTTP {e.code}: {detail}', file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f'Network error: {e.reason}', file=sys.stderr)
        sys.exit(1)
    with open(out_path, 'wb') as f:
        f.write(audio)
    print(f'Saved {len(audio)} bytes to {out_path}')


def main():
    p = argparse.ArgumentParser(description='ElevenLabs text-to-speech demo')
    p.add_argument('text', help='Text to convert to speech')
    p.add_argument('--voice-id', default='21m00Tcm4TlvDq8ikWAM', help='ElevenLabs voice ID')
    p.add_argument('--model-id', default='eleven_monolingual_v1', help='ElevenLabs model ID')
    p.add_argument('--out', default='speech.mp3', help='Output MP3 path')
    args = p.parse_args()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print('Set ELEVENLABS_API_KEY first.', file=sys.stderr)
        sys.exit(2)
    synthesize(args.text, args.voice_id, api_key, args.model_id, args.out)


if __name__ == '__main__':
    main()