# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
#
from c7n.reporter import c7n_reporter
from c7n.version import version

# Reporting
c7n_reporter.system_report(publish=True, tags=[version])
c7n_reporter.setup_excepthook(publish=True, tags=[version])
