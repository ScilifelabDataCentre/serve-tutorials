import sklearn.metrics as skl_m
import torch
from torch import nn


def train(dataloader, model, loss_fn, optimizer, device, verbose=False):
    training_losses, metrics = [], []

    for i, batch in enumerate(dataloader):
        X, y = batch['image'], batch['label']
        X, y = X.to(device), y.to(device)

        prediction = model(X)
        training_loss = loss_fn(prediction, y)

        optimizer.zero_grad()
        training_loss.backward()
        optimizer.step()

        training_loss = training_loss.item()
        y_pred = nn.Softmax(dim=1)(prediction)[:, 1]
        training_losses.append(training_loss)
        metric_score = skl_m.mean_squared_error(y.cpu().detach(),
                                                y_pred.cpu().detach())
        metrics.append(metric_score)

    training_loss = sum(training_losses) / len(training_losses)
    metric = sum(metrics) / len(metrics)

    if verbose:
        print(f"Training loss: {training_loss:>5f}, "
              f"Training metric: {metric:>5f}")

    return metric, training_loss


def validate(dataloader, model, loss_fn, device, verbose=False):
    model.eval()
    validation_losses, metrics = [], []

    with torch.no_grad():
        for i, batch in enumerate(dataloader):
            X, y = batch['image'], batch['label']
            X, y = X.to(device), y.to(device)

            prediction = model(X)
            y_pred = nn.Softmax(dim=1)(prediction)[:, 1]
            validation_losses.append(loss_fn(prediction, y).item())
            metric_score = skl_m.mean_squared_error(y.cpu().detach(),
                                                    y_pred.cpu().detach())
            metrics.append(metric_score)

    validation_loss = sum(validation_losses) / len(validation_losses)
    metric = sum(metrics)/len(metrics)

    if verbose:
        print(f"Validation loss: {validation_loss:>5f}, "
              f"Validation metric: {metric:>5f} \n")

    return metric, validation_loss
