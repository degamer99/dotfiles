#!/usr/bin/env bash

SESSION="Yt-Downloads"
echo $SESSION

tmux new-session -d -s "$SESSION"                                                                                                                                                                                    # this command is just to create a new session
tmux send-keys -t "$SESSION" "echo hello_world_top_left___Exploits && YtDownload --DownloadLocation ./Exploits/ --Link https://youtube.com/playlist?list=PLXeS5BLle0KF54wbcDVM8ErdLZrE4FsuW&si=yN44QRB_U6uLqPzP" C-m # Pane 0

tmux split-window -h -t "${SESSION}:1.1"
tmux send-keys -t "${SESSION}:1.2" "echo hello_world_top_right___Languages && YtDownload --DownloadLocation ./Language/ --Link https://youtube.com/playlist?list=PLXeS5BLle0KG7-BV_-s3PChfkK8I-tnB4&si=gLG9PiRDFe_l7ghg" C-m # Pane 0

tmux split-window -v -t "${SESSION}:1.2"
# tmux send-keys -t "${SESSION}:1.3" "echo hello_world_bottom_right___Baqarah && YtDownload --DownloadLocation ./Al-Baqarah_Tafsir/ https://youtube.com/playlist?list=PLfPaq0Tsvo5HKyez-NzUqNvtxurQRUGVV&si=aJZUOCXGaErFcayM " C-m # Pane 0

tmux split-window -v -t "${SESSION}:1.1"
tmux send-keys -t "${SESSION}:1.2" "echo hello_world_bottom_left___Tafsir-Albani && YtDownload --DownloadLocation ./Tafsir_Albani --Link https://youtube.com/playlist?list=PLImhT470ARRD1AgeJG0ErUum98OyQ3G5V&si=meqaDK7S1wmKVzpp " C-m # Pane 0

# Focus back on the top-left pane
tmux select-pane -t "${SESSION}:1.1"

# Optionally attach
tmux attach-session -t "$SESSION"
