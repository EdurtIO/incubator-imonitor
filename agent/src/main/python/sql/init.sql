create table `monitor_memory_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_memory_id` int comment '内存监控信息ID'
) comment = '主机与主机内存监控关系表';

create table `monitor_cpu_host_relation` (
    `host_id` int comment '主机ID',
    `monitor_cpu_id` int comment 'CPU监控信息ID'
) comment = '主机与主机CPU监控关系表';
