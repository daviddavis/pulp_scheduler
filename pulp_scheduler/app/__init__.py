from pulpcore.plugin import PulpPluginAppConfig


class PulpSchedulerPluginAppConfig(PulpPluginAppConfig):
    """Entry point for the pulp_scheduler plugin."""

    name = "pulp_scheduler.app"
    label = "scheduler"
    version = "0.1.0.dev"
    python_package_name = "pulp-scheduler"
    domain_compatible = True
