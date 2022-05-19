import lue.framework as lfr
from .operations import *

#~ cfg = [
#~     # Make sure hpx_main is always executed
#~     "hpx.run_hpx_main!=1",
#~     # Allow for unknown command line options
#~     "hpx.commandline.allow_unknown!=1",
#~     # Disable HPX' short options
#~     "hpx.commandline.aliasing!=1",
#~     # Don't print diagnostics during forced terminate
#~     "hpx.diagnostics_on_terminate!=0",
#~     # Make AGAS clean up resources faster than by default
#~     "hpx.agas.max_pending_refcnt_requests!=50",
#~ 
#~     # Got an HPX error when processing Africa dataset:
#~     #     mmap() failed to allocate thread stack due to
#~     #     insufficient resources, increase
#~     #     /proc/sys/vm/max_map_count or add
#~     #     -Ihpx.stacks.use_guard_pages=0 to the command line
#~     "hpx.stacks.use_guard_pages!=0"
#~ ]
#~ 
#~ lfr.start_hpx_runtime(cfg)
