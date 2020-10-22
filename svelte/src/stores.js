import { writable } from 'svelte/store';

export const library = writable({});

export const filter = writable('');

export const detail = writable(0);
