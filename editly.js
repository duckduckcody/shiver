import editly from 'editly';

// See editSpec documentation
await editly({
    outPath: './alpha.mp4',
    keepSourceAudio: true,
    clips: [
        { 
            layers: [
                { type: 'video', path: './vods/clip.mp4', },
                { type: 'video', path: './chats/chat.webm', width: 0.15, height: 0.5, resizeMode: 'contain', left: 0, top: 0 },
            ] 
        },
    ]
})

// layers: [{ type:'video', path: './vods/clip.mp4' }, { type:'video', path: './chats/chat.webm' }]