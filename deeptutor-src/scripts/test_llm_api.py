#!/usr/bin/env python3
"""
Quick LLM API smoke test.

Usage:
  python3 scripts/test_llm_api.py --prompt "Say hello"
  python3 scripts/test_llm_api.py --show-config
  python3 scripts/test_llm_api.py --direct --show-config
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env", override=False)


def _load_llm_services():
    from deeptutor.services.llm import factory
    from deeptutor.services.llm.config import clear_llm_config_cache, get_llm_config

    return factory, clear_llm_config_cache, get_llm_config


factory, clear_llm_config_cache, get_llm_config = _load_llm_services()


def _mask_key(key: str) -> str:
    if not key:
        return "(empty)"
    if len(key) <= 10:
        return "*" * len(key)
    return f"{key[:6]}...{key[-4:]}"


async def run_factory_test(prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> None:
    cfg = get_llm_config()
    print(f"[FactoryTest] model={cfg.model}")
    print("[FactoryTest] Calling factory.complete(...)")
    answer = await factory.complete(
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = (answer or "").strip()
    print(f"[FactoryTest] OK  (model={cfg.model})")
    print("[FactoryTest] Response preview:")
    print(text[:1000] if text else "(empty)")


async def run_direct_test(prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> None:
    cfg = get_llm_config()
    url = f"{(cfg.base_url or '').rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.api_key}",
    }
    payload = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    print(f"[DirectTest] POST {url}")
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(url, headers=headers, json=payload)
    print(f"[DirectTest] status={resp.status_code}")

    try:
        body = resp.json()
        print("[DirectTest] JSON response:")
        print(json.dumps(body, ensure_ascii=False, indent=2)[:4000])
    except Exception:
        print("[DirectTest] Non-JSON response:")
        print(resp.text[:2000])


async def main() -> None:
    parser = argparse.ArgumentParser(description="Quick LLM API smoke test")
    parser.add_argument("--prompt", default="Briefly explain what a derivative is.")
    parser.add_argument("--system", default="You are a concise helpful assistant.")
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--show-config", action="store_true")
    parser.add_argument(
        "--direct",
        action="store_true",
        help="Also call /chat/completions endpoint directly and print raw response.",
    )
    args = parser.parse_args()

    clear_llm_config_cache()
    cfg = get_llm_config()

    if args.show_config:
        print("[Config]")
        print(f"  binding={cfg.binding}")
        print(f"  host={cfg.base_url}")
        print(f"  model={cfg.model}")
        print(f"  max_concurrency={cfg.max_concurrency}")
        print(f"  requests_per_minute={cfg.requests_per_minute}")
        print(f"  api_key={_mask_key(cfg.api_key)}")

    try:
        await run_factory_test(args.prompt, args.system, args.max_tokens, args.temperature)
    except Exception as exc:
        print(f"[FactoryTest] FAILED: {type(exc).__name__}: {exc}")

    if args.direct:
        try:
            await run_direct_test(args.prompt, args.system, args.max_tokens, args.temperature)
        except Exception as exc:
            print(f"[DirectTest] FAILED: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
