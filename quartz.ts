import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as ExternalPlugin from "./.quartz/plugins"

// Pure numeric-aware sort by display name — folders and files interleave by
// their "N. " prefix instead of the plugin default (all folders before files).
ExternalPlugin.Explorer({
  sortFn: (a, b) => {
    return (a.displayName || "").localeCompare(b.displayName || "", undefined, {
      numeric: true,
      sensitivity: "base",
    })
  },
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
