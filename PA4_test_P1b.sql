-- CS457 PA4

-- This script includes the commands to be executed by process P1b

-- On P1:
commit; --persist the change to disk
select * from Flights;

---------------------
-- Expected output --
---------------------

-- 1 record modified.
-- Transaction committed.
-- seat int|status int
-- 22|1
-- 23|1