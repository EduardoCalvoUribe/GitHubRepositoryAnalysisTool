import { reactive } from 'vue';

/**
 * State management object for storing reactive data.
 * @type {Object}
 * @property {Object|null} githubResponse - The GitHub API response data, set to null initially.
 */
export const state = reactive({
  // Initialize githubResponse with null.
  githubResponse: null,
});
