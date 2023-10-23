#!/bin/sh

#
# Generated on Sun Oct 22 10:28:35 PDT 2023
# Start of user configurable variables
#
LANG=C
export LANG

#Trap to cleanup cookie file in case of unexpected exits.
trap 'rm -f $COOKIE_FILE; exit 1' 1 2 3 6 

# SSO username 
printf 'SSO User Name:' 
read SSO_USERNAME

# Path to wget command
WGET=/usr/bin/wget

# Log directory and file
LOGDIR=.
LOGFILE=$LOGDIR/wgetlog-$(date +%m-%d-%y-%H:%M).log

# Print wget version info 
echo "Wget version info: 
------------------------------
$($WGET -V) 
------------------------------" > "$LOGFILE" 2>&1 

# Location of cookie file 
COOKIE_FILE=$(mktemp -t wget_sh_XXXXXX) >> "$LOGFILE" 2>&1 
if [ $? -ne 0 ] || [ -z "$COOKIE_FILE" ] 
then 
 echo "Temporary cookie file creation failed. See $LOGFILE for more details." |  tee -a "$LOGFILE" 
 exit 1 
fi 
echo "Created temporary cookie file $COOKIE_FILE" >> "$LOGFILE" 

# Output directory and file
OUTPUT_DIR=.
#
# End of user configurable variable
#

# The following command to authenticate uses HTTPS. This will work only if the wget in the environment
# where this script will be executed was compiled with OpenSSL.
# 
 $WGET  --secure-protocol=auto --save-cookies="$COOKIE_FILE" --keep-session-cookies --http-user "$SSO_USERNAME" --ask-password  "https://edelivery.oracle.com/osdc/cliauth" -a "$LOGFILE"

# Verify if authentication is successful 
if [ $? -ne 0 ] 
then 
 echo "Authentication failed with the given credentials." | tee -a "$LOGFILE"
 echo "Please check logfile: $LOGFILE for more details." 
else
 echo "Authentication is successful. Proceeding with downloads..." >> "$LOGFILE" 
 $WGET --load-cookies="$COOKIE_FILE" "https://edelivery.oracle.com/ocom/softwareDownload?fileName=V997917-01.zip&token=SDhGUkNVbTNLU2ExTGxKZFhhVmJadyE6OiFmaWxlSWQ9MTA4NjU4OTk4JmZpbGVTZXRDaWQ9OTY5OTM0JnJlbGVhc2VDaWRzPTk2OTM5OCZkb3dubG9hZFR5cGU9OTU3NjEmYWdyZWVtZW50SWQ9MTAxMzI3MTcmZW1haWxBZGRyZXNzPXVwMjAyMDA1Mjc3QGVkdS5mZS51cC5wdCZ1c2VyTmFtZT1FUEQtVVAyMDIwMDUyNzdARURVLkZFLlVQLlBUJmlwQWRkcmVzcz05NC42MC4yMTMuMTIwJnVzZXJBZ2VudD1Nb3ppbGxhLzUuMCAoWDExOyBVYnVudHU7IExpbnV4IHg4Nl82NDsgcnY6MTA5LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTE4LjAmY291bnRyeUNvZGU9UFQmZGxwQ2lkcz0xMDQ4NDA3JmFwcGxpY2F0aW9uSWQ9OSZzc295bj1ZJnF1ZXJ5U3RyaW5nPWRscF9jaWQsMTA0ODQwNyFyZWxfY2lkLDk2OTM5OA" -O "$OUTPUT_DIR/V997917-01.zip" >> "$LOGFILE" 2>&1 
fi 

# Cleanup
rm -f "$COOKIE_FILE" 
echo "Removed temporary cookie file $COOKIE_FILE" >> "$LOGFILE" 

