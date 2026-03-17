Issue:
EMERGENCY->HOT直後にHOT->WARMが即発生。

Root cause:
stable_timeが状態遷移後も保持されていた。

Fix introduced in:
v0.3
