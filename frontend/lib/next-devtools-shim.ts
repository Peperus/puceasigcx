import { createContext, useContext } from "react";

type Dispatcher = Record<string, (...args: unknown[]) => void>;

export const dispatcher = new Proxy<Dispatcher>(
  {},
  {
    get() {
      return () => {};
    },
  },
);

export const DevOverlayContext = createContext(null);

export function renderAppDevOverlay() {}

export function renderPagesDevOverlay() {}

export function useDevOverlayContext() {
  return useContext(DevOverlayContext);
}

export function getSegmentTrieData() {
  return null;
}

export function getSerializedOverlayState() {
  return null;
}
