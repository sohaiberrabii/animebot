# AnimeBot

Rasa bot that search for anime using the [Jikan](https://jikan.docs.apiary.io/) API.

The user can specify the anime **genre**, **rating** and whether to sort the search **by popularity**.

The **happy paths** are handled by `Form` (anime_form) and the `Custom Action` (action_search_anime).
`Rules` are used to activate the form or call this action. 

Three different types of **unhappy paths** are handled:
* Wrong answers to the form's requested slots
* Chitchat or Bot challenge instead of answering form questions
* User asks to stop/cancel the form

The first type is handled by a `FormValidationAction`. For example, 
if the user asks for an anime genre that isn't handled, the assistant will
answer by listing the allowed genres.


The second type is handled mainly using `Rules`, but also some `Stories`
that were generated using `rasa interactive`.

The third type of unhappy paths is handled using two general `Stories`
and multiple interactive stories.

## Basic Usage

Training the assistant

```
rasa train
```

Interaction with the assistant
```
rasa run actions&
rasa shell
```

## Examples

### Happy path
[happy path](happy_path.png)

### Un-Happy path (Stop the form then continue)
[unhappy_path](unhappy_path_stop_continue.png)

## Note
Sometimes the API call fails, I should have picked a more reliable API :(