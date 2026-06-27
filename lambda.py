#lambda function for deleting unused snapshots



import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# AWS EC2 Client
ec2 = boto3.client("ec2")

# Retention Period (Days)
RETENTION_DAYS = 30


def lambda_handler(event, context):

    print("=" * 80)
    print("Starting EBS Snapshot Cleanup")
    print("=" * 80)

    deleted = 0
    skipped = 0
    failed = 0

    # ------------------------------------------------------------------
    # List Running and Stopped EC2 Instances
    # ------------------------------------------------------------------

    instance_response = ec2.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running", "stopped"]
            }
        ]
    )

    print("\n" + "=" * 80)
    print("EC2 Instance Inventory")
    print("=" * 80)

    total_instances = 0

    for reservation in instance_response["Reservations"]:
        for instance in reservation["Instances"]:

            total_instances += 1

            instance_id = instance["InstanceId"]
            instance_state = instance["State"]["Name"]

            instance_name = "N/A"

            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
                    break

            print(f"Instance Name : {instance_name}")
            print(f"Instance ID   : {instance_id}")
            print(f"State         : {instance_state}")
            print("-" * 80)

    print(f"Total EC2 Instances : {total_instances}")

    # ------------------------------------------------------------------
    # Get All Snapshots
    # ------------------------------------------------------------------

    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"]
    )["Snapshots"]

    print("\n" + "=" * 80)
    print("Snapshot Inventory")
    print("=" * 80)

    print(f"Total Snapshots Found : {len(snapshots)}")

    # ------------------------------------------------------------------
    # Process Each Snapshot
    # ------------------------------------------------------------------

    for snapshot in snapshots:

        snapshot_id = snapshot["SnapshotId"]
        volume_id = snapshot.get("VolumeId")

        snapshot_age = (
            datetime.now(timezone.utc) - snapshot["StartTime"]
        ).days

        print("\n" + "-" * 80)
        print(f"Snapshot ID : {snapshot_id}")
        print(f"Volume ID   : {volume_id}")
        print(f"Age         : {snapshot_age} Days")

        # --------------------------------------------------------------
        # Skip New Snapshots
        # --------------------------------------------------------------

        if snapshot_age < RETENTION_DAYS:

            skipped += 1

            print(
                f"Skipped : Snapshot is newer than "
                f"{RETENTION_DAYS} days."
            )

            continue

        # --------------------------------------------------------------
        # Snapshot Has No Volume
        # --------------------------------------------------------------

        if not volume_id:

            try:

                ec2.delete_snapshot(
                    SnapshotId=snapshot_id
                )

                deleted += 1

                print(
                    "Deleted : Snapshot has no associated volume."
                )

            except ClientError as e:

                failed += 1

                print(f"Error : {e}")

            continue

        # --------------------------------------------------------------
        # Check Whether Volume Exists
        # --------------------------------------------------------------

        try:

            volume = ec2.describe_volumes(
                VolumeIds=[volume_id]
            )["Volumes"][0]

        except ClientError as e:

            if e.response["Error"]["Code"] == "InvalidVolume.NotFound":

                try:

                    ec2.delete_snapshot(
                        SnapshotId=snapshot_id
                    )

                    deleted += 1

                    print(
                        "Deleted : Associated volume no longer exists."
                    )

                except ClientError as err:

                    failed += 1

                    print(err)

                continue

            failed += 1

            print(e)

            continue

        # --------------------------------------------------------------
        # Check Attachment
        # --------------------------------------------------------------

        attachments = volume.get("Attachments", [])

        if len(attachments) == 0:

            try:

                ec2.delete_snapshot(
                    SnapshotId=snapshot_id
                )

                deleted += 1

                print(
                    f"Deleted : Volume {volume_id} is detached."
                )

            except ClientError as e:

                failed += 1

                print(e)

        else:

            skipped += 1

            instance_id = attachments[0]["InstanceId"]

            print(
                f"Skipped : Volume is attached to EC2 Instance "
                f"{instance_id}"
            )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("Cleanup Summary")
    print("=" * 80)

    print(f"Total Snapshots : {len(snapshots)}")
    print(f"Deleted         : {deleted}")
    print(f"Skipped         : {skipped}")
    print(f"Failed          : {failed}")

    print("=" * 80)

    return {
        "statusCode": 200,
        "body": "Snapshot cleanup completed successfully."
    }


if __name__ == "__main__":
    lambda_handler({}, {})