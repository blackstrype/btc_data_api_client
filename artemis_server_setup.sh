#!/bin/bash
IMAGE_ID=$(hcloud image list --type=snapshot | grep "artemis-1" | head -n 1 | awk '{print $1}')

if [ -z "$IMAGE_ID" ]; then
    echo "❌ Error: No Artemis snapshot found. Have you taken one yet?"
    exit 1
fi

echo "🚀 Provisioning Mission Lab from Snapshot: $IMAGE_ID..."

hcloud server create \
    --name artemis-1 \
    --image "$IMAGE_ID" \
    --type cpx22 \
    --location hel1 \
    --ssh-key blackstrype.pub \
    --firewall base-firewall \
    --firewall artemis-messaging

echo "✅ Server is booting. Run 'hcloud server list' to get the new IP."
