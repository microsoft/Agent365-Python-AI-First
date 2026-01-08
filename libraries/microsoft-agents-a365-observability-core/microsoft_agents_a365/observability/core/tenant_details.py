# Copyright (c) Microsoft. All rights reserved.

# Tenant details class.
from dataclasses import dataclass


@dataclass
class TenantDetails:
    """Represents the tenant id attached to the span."""

    tenant_id: str
