#!/bin/bash

function is_docker_vm {
    getent hosts host.docker.internal >/dev/null 2>&1
    return $?
}

function get_vm_host_ip {
    if ! is_docker_vm; then
        echo "ERROR: this is not running from a docker VM!"
        exit 1
    fi

    echo "$(getent hosts host.docker.internal | awk '{ print $1 }')"
}

# Set udp port from input. This way we can use --network host, but define different udp ports for mavlink-routerd
udp_offboard_port_remote=$1

# Broadcast doesn't work with docker from a VM (macOS or Windows), so we default to the vm host (host.docker.internal)
if is_docker_vm; then
    VM_HOST=$(get_vm_host_ip)
    QGC_PARAM=${QGC_PARAM:-"-t ${VM_HOST}"}
    API_PARAM=${API_PARAM:-"-t ${VM_HOST}"}
fi

CONFIG_FILE=${FIRMWARE_DIR}/ROMFS/px4fmu_common/init.d-posix/rcS

sed -i "s/mavlink start \-x \-u \$udp_gcs_port_local -r 4000000/mavlink start -x -u \$udp_gcs_port_local -r 4000000 ${QGC_PARAM}/" ${CONFIG_FILE}
sed -i "s/mavlink start \-x \-u \$udp_offboard_port_local -r 4000000 -m onboard -o \$udp_offboard_port_remote/mavlink start -x -u \$udp_offboard_port_local -r 4000000 -o $udp_offboard_port_remote ${API_PARAM}/" ${CONFIG_FILE}

# Parameters
echo 'param set MAV_BROADCAST 1' >> ${CONFIG_FILE}

echo 'param set MIS_DIST_WPS 0' >> ${CONFIG_FILE}
echo 'param set MIS_DIST_1WP 0' >> ${CONFIG_FILE}

## MPC
echo 'param set MPC_XY_CRUISE 10' >> ${CONFIG_FILE}
echo 'param set MPC_POS_MODE 1' >> ${CONFIG_FILE}

echo 'param set MPC_ACC_DOWN_MAX	4' >> ${CONFIG_FILE}
echo 'param set MPC_ACC_HOR	5' >> ${CONFIG_FILE}

echo 'param set MPC_ACC_HOR_MAX 10' >> ${CONFIG_FILE}
echo 'param set MPC_ACC_UP_MAX 10' >> ${CONFIG_FILE}

# Failsafe(s)
echo 'param set COM_LOW_BAT_ACT 2' >> ${CONFIG_FILE}
echo 'param set NAV_RCL_ACT 0' >> ${CONFIG_FILE}
echo 'param set COM_OF_LOSS_T	0' >> ${CONFIG_FILE}

############################
# Pre-arm check (disabled) #
############################

# Disable PRE-ARM mode
echo 'param set COM_PREARM_MODE	0' >> ${CONFIG_FILE}

# Maximum accelerometer inconsistency
echo 'param set COM_ARM_IMU_ACC 1' >> ${CONFIG_FILE}

# Maximum rate gyro inconsistency
echo 'param set COM_ARM_IMU_GYR 0.3' >> ${CONFIG_FILE}

# Maximum magnetic field inconsistency
echo 'param set COM_ARM_MAG_ANG	-1' >> ${CONFIG_FILE}

# Maximum EKF innovation test ratio
echo 'param set COM_ARM_EKF_AB	0.01' >> ${CONFIG_FILE}
echo 'param set COM_ARM_EKF_GB	0.0017' >> ${CONFIG_FILE}
echo 'param set COM_ARM_EKF_HGT	1.0' >> ${CONFIG_FILE}
echo 'param set COM_ARM_EKF_POS	1.0' >> ${CONFIG_FILE}
echo 'param set COM_ARM_EKF_VEL	1.0' >> ${CONFIG_FILE}
echo 'param set COM_ARM_EKF_YAW	1.0' >> ${CONFIG_FILE}


############################
# Mavlink                  #
############################

# Mavlink version (use mavlink 1 only)
echo 'param set MAV_PROTO_VER 1' >> ${CONFIG_FILE}
